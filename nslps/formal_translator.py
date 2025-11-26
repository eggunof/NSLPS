import asyncio
import json
import os

from dotenv import load_dotenv

from nslps.abstract_formal_translator import AbstractFormalTranslator
from nslps.contracts import ResolveAxiomsIntoGoalRequest, ResolveAxiomsIntoGoalResponse
from nslps.formal_language.fundamentals import FormalStatement
from nslps.formal_language.proofing import (
    ResolveAxiomsIntoGoalResult,
    ResolveAxiomsIntoGoalTask,
    ProofStep,
)

import aiohttp

load_dotenv()


class FormalTranslator(AbstractFormalTranslator):
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL")
        # Выбрать другую модель можно тут https://openrouter.ai/models

    async def translate_natural_to_resolve_axioms_into_goal_command(
        self, statement: ResolveAxiomsIntoGoalRequest
    ) -> ResolveAxiomsIntoGoalTask:
        """
        Translates natural language into command.

        :param statement: Natural language statement to translate
        :return: Command in formal language
        """
        async with aiohttp.ClientSession() as session:
            response = await session.request(
                "POST",
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                data=json.dumps(
                    {
                        "model": self.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": """Ты — экспертный ассистент по формальной логике. Выведи ТОЛЬКО формулы в формате: Предикат(Объект) или ¬Предикат(Объект) разделяя их запятыми. Утвереждение, которое необходимо доказать - должно быть последним. ОБЯЗАТЕЛЬНО. Преобразуй следующую текстовую задачу:""",
                            },
                            {"role": "user", "content": str(statement)},
                        ],
                    }
                ),
            )
            text = (await response.json()).get("choices")[0].get("message").get("content")
            statements = text.split(",")
            result = []
            for statement in statements:
                statement = statement.strip()
                statement = FormalStatement().parse(statement)
                result.append(statement)
        return ResolveAxiomsIntoGoalTask(axioms=result[:-1], goal=result[-1])

    async def translate_resolve_axioms_into_goal_result_to_natural(
        self, result: ResolveAxiomsIntoGoalResult
    ) -> ResolveAxiomsIntoGoalResponse:
        """
        Turns result of the command into a text in natural language.

        :param result: Result to translate
        :return: Natural language text
        """
        async with aiohttp.ClientSession() as session:
            response = await session.request(
                "POST",
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                data=json.dumps(
                    {
                        "model": self.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": """
                                Ты — учитель логики. Объясни доказательство, представленное в виде последовательности логических шагов, как если бы ты объяснял его студенту. Будь последовательным и ясным. Используй естественный русский язык. Переведи логические высказывания в естественные слова. Пример:
                                [Шаг 1: Унификация {x/Сократ} в ¬Человек(x) ∨ Смертен(x). Шаг 2: Резолюция с Человек(Сократ) -> Смертен(Сократ). Шаг 3: Резолюция Смертен(Сократ) и ¬Смертен(Сократ) -> Противоречие.]
                                Выход (объяснение): "Давайте разберем доказательство по шагам. У нас есть общее правило: 'Если кто-то является человеком, то он смертен'. Мы применяем это правило к Сократу, подставляя его вместо переменной 'x'. Поскольку нам также известно, что Сократ — человек, мы приходим к выводу, что Сократ смертен. Но это противоречит нашему исходному предположению, что Сократ не является смертным. Это противоречие доказывает, что наше предположение было ложным, а значит, Сократ действительно смертен.
                                ВАЖНО: Отделяй каждый этап объяснений символом переноса строки. Избегай использования разметок (таких как MarkDown)
                                """,
                            },
                            {
                                "role": "user",
                                "content": f"{str(result.is_proven)} {''.join([str(item) for item in result.steps])}",
                            },
                        ],
                    }
                ),
            )
            text = (await response.json()).get("choices")[0].get("message").get("content")

            steps = []
            for step in text.split("\n"):
                step = step.strip()
                if len(step) > 1:
                    steps.append(step)

            return ResolveAxiomsIntoGoalResponse(is_proven=result.is_proven, steps=steps)


async def main():

    task = ResolveAxiomsIntoGoalRequest(
        text="Сократ — человек. Все люди смертны. Докажи, что Сократ смертен."
    )
    cl = FormalTranslator()

    # result = await cl.translate_natural_to_resolve_axioms_into_goal_command(task)
    axioms = ResolveAxiomsIntoGoalResult(
        is_proven=True,
        steps=[
            ProofStep(action="Шаг 1: Унификация {x/Сократ} в ¬Человек(x) ∨ Смертен(x)"),
            ProofStep(action="Шаг 2: Резолюция с Человек(Сократ) -> Смертен(Сократ)"),
            ProofStep(action="Шаг 3: Резолюция Смертен(Сократ) и ¬Смертен(Сократ)"),
            ProofStep(action="Противоречие"),
        ],
    )
    result = await cl.translate_resolve_axioms_into_goal_result_to_natural(axioms)
    print(result.is_proven)
    print(result.steps)


if __name__ == "__main__":
    asyncio.run(main())

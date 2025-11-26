import os
from typing import cast

from dotenv import load_dotenv
from openrouter import OpenRouter

from nslps.formal_language.fundamentals import Clause
from nslps.formal_language.parsing.formula_parser import FormulaParser
from nslps.formal_language.proofing import ResolutionResult
from nslps.llm_provider import LLMProvider

load_dotenv()


class MockLLM(LLMProvider):
    """
    A mock implementation of the LLM for demonstration and testing purposes.
    Simulates the parsing of the Socrates example without actual API calls.
    """

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL")
        self.parser = FormulaParser()

    async def formalize(self, text: str) -> tuple[list[Clause], Clause]:
        """
        Simulates the LLM's API response (as raw text) and then parses it.
        """
        print(f"\n[LLM-Formalizer] Processing text: '{text}'...")

        # --- 1. Simulated LLM API Output (Raw String) ---
        # The LLM's output is expected to be a single string of comma-separated statements.
        response = await self._send_request(
            [
                {
                    "role": "system",
                    "content": """
                        Ты — экспертный ассистент по формальной логике.
                        Выведи ТОЛЬКО формулы в формате:
                        Предикат(Объект) или ¬Предикат(Объект)
                        разделяя их запятыми.
                        Утвереждение, которое необходимо доказать - должно быть
                        последним. ОБЯЗАТЕЛЬНО.
                        Преобразуй следующую текстовую задачу:
                        """,
                },
                {"role": "user", "content": text},
            ]
        )
        print(response)
        statements = [statement.strip() for statement in response.split(",")]
        raw_kb_output = statements[::-1]
        raw_goal_output = statements[-1]

        print(f"  > Simulated LLM KB Output: '{raw_kb_output}'")
        print(f"  > Simulated LLM Goal Output: '{raw_goal_output}'")

        # --- 2. Parsing (Using the FormulaParser) ---

        # Knowledge Base: Multiple clauses separated by commas
        kb_clauses = self.parser.parse_clauses_from_raw_string(raw_kb_output)

        # Goal: A single clause that represents the query
        # We assume the goal is a single literal query, hence we take the first element [0]
        try:
            goal_clause = self.parser.parse_clauses_from_raw_string([raw_goal_output])[0]
        except IndexError:
            # Handle case where the goal output is empty or malformed
            raise ValueError("LLM failed to output a valid goal statement for parsing.")

        return kb_clauses, goal_clause

    async def explain(self, result: ResolutionResult) -> str:
        """
        Simulates generating a human-readable explanation from the log.
        """

        print(f"\n[LLM-Explainer] Analyzing {len(result.proof_log)} proof steps...")

        response = await self._send_request(
            [
                {
                    "role": "system",
                    "content": """
                        Ты — учитель логики. Объясни доказательство,
                        представленное в виде последовательности
                        логических шагов, как если бы ты объяснял его
                        студенту. Будь последовательным и ясным.
                        Используй естественный русский язык.
                        Переведи логические высказывания в естественные
                        слова. Пример:
                        [Шаг 1: Унификация {x/Сократ} в ¬Человек(x) ∨
                        Смертен(x). Шаг 2: Резолюция с Человек(Сократ)
                        -> Смертен(Сократ). Шаг 3: Резолюция Смертен(Сократ)
                        и ¬Смертен(Сократ) -> Противоречие.]
                        Выход (объяснение):
                        "Давайте разберем доказательство по шагам.
                        У нас есть общее правило: 'Если кто-то является
                        человеком, то он смертен'. Мы применяем это правило
                        к Сократу, подставляя его вместо переменной 'x'.
                        Поскольку нам также известно, что Сократ — человек,
                        мы приходим к выводу, что Сократ смертен. Но это
                        противоречит нашему исходному предположению, что
                        Сократ не является смертным. Это противоречие
                        доказывает, что наше предположение было ложным, а
                        значит, Сократ действительно смертен.
                        ВАЖНО: Отделяй каждый этап объяснений символом
                        переноса строки. Избегай использования разметок
                        (таких как MarkDown)
                        """,
                },
                {
                    "role": "user",
                    "content": f"IS_PROVEN:{str(result.is_proven)} {''.join([str(item) for item in result.proof_log])}",
                },
            ]
        )

        steps = ""
        for step in response.split("\n"):
            step = step.strip()
            if len(step) > 1:
                steps += step

        return steps

    async def _send_request(self, messages: list[dict[str, str]]) -> str:
        """
        Sends a request to the LLM API and returns the response.
        Returns None if the request fails.
        """
        with OpenRouter(api_key=self.api_key) as client:
            response = client.chat.send(model=self.model, messages=messages)
            return cast(str, response.choices[0].message.content)

import json
import logging
import os
from pathlib import Path
from typing import cast

from dotenv import load_dotenv
from openrouter import OpenRouter
from openrouter.errors import ChatError

from nslps.formal_language.fundamentals import Clause
from nslps.formal_language.parsing.formula_parser import FormulaParser
from nslps.formal_language.proofing import ResolutionResult
from nslps.llm_exception import LLMException
from nslps.llm_provider import LLMProvider

load_dotenv()

logger = logging.getLogger(__name__)


class OpenRouterLLM(LLMProvider):
    """
    A mock implementation of the LLM for demonstration and testing purposes.
    Simulates the parsing of the Socrates example without actual API calls.
    """

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL")
        self.parser = FormulaParser()
        self._load_prompts()

    def _load_prompts(self) -> None:
        """
        Loads system prompts from prompts.json, assuming the file is located
        in the same directory as this module.
        """
        file_path = Path(__file__).parent / "prompts.json"

        if not file_path.exists():
            logger.error("Prompt file prompts.json not found at path: %s", file_path)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                prompts = json.load(f)
                self.formalizer_prompt = prompts.get("formalizer")
                self.explainer_prompt = prompts.get("explainer")
        except json.JSONDecodeError as e:
            logger.error("Error decoding prompts.json: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error while reading prompts.json: %s", e)
            raise

    async def formalize(self, text: str) -> tuple[list[Clause], Clause]:
        """
        Simulates the LLM's API response (as raw text) and then parses it.
        """
        logger.info("[LLM-Formalizer] processing text: '%s'...", text)

        response = await self._send_request(
            [
                {"role": "system", "content": self.formalizer_prompt},
                {"role": "user", "content": text},
            ]
        )
        logger.debug("LLM formalizer response: '%s'", response)
        statements = [statement.strip() for statement in response.split(",")]
        axioms = statements[:-1]
        goal = statements[-1]

        logger.info("[LLM-Formalizer] Axioms output: %s", "; ".join(axioms))
        logger.info("[LLM-Formalizer] Goal Output: %s", goal)

        axioms_clauses = [self.parser.parse_clause(axiom) for axiom in axioms]
        goal_clause = self.parser.parse_clause(goal)

        return axioms_clauses, goal_clause

    async def explain(self, result: ResolutionResult) -> str:
        """
        Simulates generating a human-readable explanation from the log.
        """

        logger.info("LLM-Explainer analyzing %d proof steps...", len(result.proof_log))

        message = (
            f"IS_PROVEN:{str(result.is_proven)} {''.join([str(item) for item in result.proof_log])}"
        )
        response = await self._send_request(
            [
                {"role": "system", "content": self.explainer_prompt},
                {"role": "user", "content": message},
            ]
        )
        logger.debug("LLM-Explainer response: %s", response)

        return response.strip()

    async def _send_request(self, messages: list[dict[str, str]]) -> str:
        """
        Sends a request to the LLM API and returns the response.
        Returns None if the request fails.
        """
        try:
            with OpenRouter(api_key=self.api_key) as client:
                response = client.chat.send(model=self.model, messages=messages)
                return cast(str, response.choices[0].message.content)
        except ChatError as e:
            logger.error("OpenRouter error: %s", e)
            raise LLMException() from e

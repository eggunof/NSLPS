from abc import ABC, abstractmethod

from nslps.formal_language.fundamentals import Clause
from nslps.formal_language.proofing import ResolutionResult


class LLMProvider(ABC):
    """
    Abstract interface for interacting with Large Language Models.
    """

    @abstractmethod
    async def formalize(self, text: str) -> tuple[list[Clause], Clause]:
        """
        Module 1: Translates natural language text into logical clauses and a goal.
        Returns (KnowledgeBase, Goal).
        """

    @abstractmethod
    async def explain(self, result: ResolutionResult) -> str:
        """
        Module 3: Translates the formal proof log back into natural language.
        """

from abc import ABC, abstractmethod

from nslps.contracts import ResolveAxiomsIntoGoalRequest, ResolveAxiomsIntoGoalResponse
from nslps.formal_language.proofing import ResolveAxiomsIntoGoalCommand, ResolveAxiomsIntoGoalResult


class AbstractFormalTranslator(ABC):
    """
    Abstract class for a translation from natural language to formal and vice versa.
    """

    @abstractmethod
    async def translate_natural_to_resolve_axioms_into_goal_command(
        self, statement: ResolveAxiomsIntoGoalRequest
    ) -> ResolveAxiomsIntoGoalCommand:
        """
        Translates natural language into command.
        
        :param statement: Natural language statement to translate 
        :return: Command in formal language
        """

    @abstractmethod
    async def translate_resolve_axioms_into_goal_result_to_natural(
        self, result: ResolveAxiomsIntoGoalResult
    ) -> ResolveAxiomsIntoGoalResponse:
        """
        Turns result of the command into a text in natural language.
        
        :param result: Result to translate 
        :return: Natural language text
        """

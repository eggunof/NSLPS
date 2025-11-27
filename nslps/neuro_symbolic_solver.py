import logging

from nslps.formal_language.proofing import ResolutionEngine
from nslps.llm_provider import LLMProvider

logger = logging.getLogger(__name__)


class NeuroSymbolicSolver:
    """
    The Orchestrator.
    Connects the Neural component (LLM) and the Symbolic component (Resolution Engine).
    """

    def __init__(self, llm: LLMProvider, engine: ResolutionEngine):
        self.llm = llm
        self.engine = engine

    async def process_query(self, user_text: str) -> str:
        """
        Full pipeline execution:
        Text → Logic → Proof → Explanation → Text
        """
        # Phase 1: Formalization (Neuro)
        logger.debug("--- Phase 1: Formalization ---")
        axioms, goal = await self.llm.formalize(user_text)
        logger.info("Knowledge Base:")
        for axiom in axioms:
            logger.info("  - %s", axiom)
        logger.info("Goal to prove: %s", goal)

        # Phase 2: Reasoning (Symbolic)
        logger.debug("--- Phase 2: Symbolic Reasoning ---")
        result = self.engine.solve(axioms, goal)
        logger.debug(
            "Proof Log: %s",
            [str(step) for step in result.proof_log],
        )

        if result.is_proven:
            logger.info("Status: PROVEN")
        else:
            logger.info("Status: NOT PROVEN")

        # Phase 3: Explanation (Neuro)
        logger.debug("--- Phase 3: Natural Language Explanation ---")
        final_answer = await self.llm.explain(result)

        return final_answer

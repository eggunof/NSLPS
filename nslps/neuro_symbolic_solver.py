from nslps.formal_language.fundamentals import Clause
from nslps.formal_language.proofing import ResolutionEngine
from nslps.llm_provider import LLMProvider


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
        print("--- Phase 1: Formalization ---")
        kb, goal = await self.llm.formalize(user_text)
        self._print_formalization(kb, goal)

        # Phase 2: Reasoning (Symbolic)
        print("\n--- Phase 2: Symbolic Reasoning ---")
        result = self.engine.solve(kb, goal)

        if result.is_proven:
            print("Status: PROVEN ✅")
        else:
            print("Status: NOT PROVEN ❌")
            return "Could not prove the statement."

        # Phase 3: Explanation (Neuro)
        print("\n--- Phase 3: Natural Language Explanation ---")
        final_answer = await self.llm.explain(result)

        return final_answer

    @staticmethod
    def _print_formalization(kb: list[Clause], goal: Clause) -> None:
        print("Knowledge Base:")
        for c in kb:
            print(f"  - {c}")
        print(f"Goal to prove: {goal}")

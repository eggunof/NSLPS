import asyncio

from nslps.formal_language.proofing import ResolutionEngine
from nslps.mock_llm import MockLLM
from nslps.neuro_symbolic_solver import NeuroSymbolicSolver


def main() -> None:
    """Main"""
    llm_service = MockLLM()
    resolution_engine = ResolutionEngine()

    solver = NeuroSymbolicSolver(llm_service, resolution_engine)

    # Example Scenario
    input_text = "Socrates is a man. All men are mortal. Prove Socrates is mortal."

    print(f"User Query: {input_text}\n")
    response = asyncio.run(solver.process_query(input_text))

    print("\n--- Final Output ---")
    print(response)


if __name__ == "__main__":
    main()

import asyncio
import logging

from nslps.formal_language.proofing import ResolutionEngine
from nslps.neuro_symbolic_solver import NeuroSymbolicSolver
from nslps.openrouter_llm import OpenRouterLLM

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main() -> None:
    """Main"""
    llm_service = OpenRouterLLM()
    resolution_engine = ResolutionEngine()

    solver = NeuroSymbolicSolver(llm_service, resolution_engine)

    input_text = input("Введите задачу: ")
    response = asyncio.run(solver.process_query(input_text))
    print(response)


if __name__ == "__main__":
    main()

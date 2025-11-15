from dataclasses import dataclass

from nslps.formal_language.proofing.proof_step import ProofStep


@dataclass(frozen=True)
class ResolveAxiomsIntoGoalResult:
    """
    Result of the command to resolve axioms into goal.
    """
    is_proven: bool
    steps: tuple[ProofStep]

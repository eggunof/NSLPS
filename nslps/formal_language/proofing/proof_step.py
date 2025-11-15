from dataclasses import dataclass


@dataclass(frozen=True)
class ProofStep:
    """
    Represents a proof step.
    """
    action: str

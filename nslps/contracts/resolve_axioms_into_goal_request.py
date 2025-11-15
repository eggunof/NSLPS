from dataclasses import dataclass


@dataclass(frozen=True)
class ResolveAxiomsIntoGoalRequest:
    """
    Request to resolve axioms into goal.
    """
    text: str

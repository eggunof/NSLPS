from dataclasses import dataclass


@dataclass(frozen=True)
class ResolveAxiomsIntoGoalResponse:
    """
    Response to resolve axioms into goal.
    """

    is_proven: bool
    steps: list[str]

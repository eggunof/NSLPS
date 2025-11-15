from dataclasses import dataclass

from nslps.formal_language.fundamentals import FormalStatement


@dataclass(frozen=True)
class ResolveAxiomsIntoGoalTask:
    """
    Command to resolve axioms into goal.
    """
    axioms: list[FormalStatement]
    goal: FormalStatement

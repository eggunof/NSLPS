from dataclasses import dataclass

from nslps.formal_language.fundamentals.literal import Literal


@dataclass
class Clause:
    """
    Represents a disjunction of literals (CNF clause).
    Example: ¬Human(x) ∨ Mortal(x)
    """

    literals: list[Literal]

    def __str__(self) -> str:
        return " ∨ ".join(str(l) for l in self.literals)

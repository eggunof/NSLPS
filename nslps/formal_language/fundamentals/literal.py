from __future__ import annotations

from dataclasses import dataclass

from nslps.formal_language.fundamentals.predicate import Predicate


@dataclass(frozen=True)
class Literal:
    """
    Represents a literal (positive or negative predicate).
    Example: Human(x) or ~Mortal(x)
    """

    predicate: Predicate
    is_negated: bool = False

    def __str__(self) -> str:
        prefix = "¬" if self.is_negated else ""
        return f"{prefix}{self.predicate}"

    @property
    def negation(self) -> Literal:
        """Returns the negation of the current literal."""
        return Literal(self.predicate, not self.is_negated)

from dataclasses import dataclass

from nslps.formal_language.fundamentals.term import Term


@dataclass(frozen=True)
class Literal:
    """
    Represents a literal.
    """
    is_negative: bool
    predicate: str
    terms: tuple[Term]

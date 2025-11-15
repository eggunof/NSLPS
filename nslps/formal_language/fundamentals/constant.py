from dataclasses import dataclass

from nslps.formal_language.fundamentals.term import Term


@dataclass(frozen=True)
class Constant(Term):
    """
    Represents a constant.
    """

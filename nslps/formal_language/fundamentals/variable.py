from dataclasses import dataclass

from nslps.formal_language.fundamentals.term import Term


@dataclass(frozen=True)
class Variable(Term):
    """
    Represents a variable.
    """

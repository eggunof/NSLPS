from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class Term(ABC):
    """
    Represents a term: a constant or a variable.
    """

    name: str

    def __str__(self) -> str:
        return self.name

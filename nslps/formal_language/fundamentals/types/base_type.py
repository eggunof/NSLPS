from dataclasses import dataclass
from typing import final

from nslps.formal_language.fundamentals.types.type_expression import TypeExpression


@final
@dataclass(frozen=True)
class BaseType(TypeExpression):
    """
    Base types: custom sorts (e.g., 'Person', 'Music') or 't' for truth values.
    In many-sorted logic, sorts are user-defined base types.
    """

    name: str  # Any valid identifier, no restrictions

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseType) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

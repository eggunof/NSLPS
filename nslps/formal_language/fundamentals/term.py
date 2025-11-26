from dataclasses import dataclass


@dataclass(frozen=True)
class Term:
    """Represents a term in predicate logic (constant or variable)."""

    name: str
    is_variable: bool

    def __str__(self) -> str:
        return self.name

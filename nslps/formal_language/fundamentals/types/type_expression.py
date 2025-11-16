from abc import ABC, abstractmethod


class TypeExpression(ABC):
    """
    Abstract base class for type expressions in higher-order logic.
    Types are recursively defined: base types (custom sorts or 't' for truth values),
    and function types from tuples of types to a type.
    """

    @abstractmethod
    def __str__(self) -> str:
        """String representation of the type."""

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Equality check for types."""

    @abstractmethod
    def __hash__(self) -> int:
        """Hash for types to allow use in dictionaries."""

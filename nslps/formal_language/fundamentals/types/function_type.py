from dataclasses import dataclass
from typing import final

from nslps.formal_language.fundamentals.types.type_expression import TypeExpression


@final
@dataclass(frozen=True)
class FunctionType(TypeExpression):
    """
    Function type: from a tuple of argument types to a result type.
    Arity is the length of arg_types (n >= 1).
    """

    arg_types: tuple[TypeExpression, ...]  # Non-empty tuple
    result_type: TypeExpression

    def __post_init__(self) -> None:
        if not self.arg_types:
            raise ValueError("FunctionType must have at least one argument type.")

    def __str__(self) -> str:
        arg_str = ", ".join(str(t) for t in self.arg_types)
        return f"<[{arg_str}], {self.result_type}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FunctionType):
            return False
        return self.arg_types == other.arg_types and self.result_type == other.result_type

    def __hash__(self) -> int:
        return hash((self.arg_types, self.result_type))

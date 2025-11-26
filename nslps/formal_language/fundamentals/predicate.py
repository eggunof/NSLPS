from dataclasses import dataclass

from nslps.formal_language.fundamentals.term import Term


@dataclass(frozen=True)
class Predicate:
    """
    Represents an atomic formula (e.g., Human(Socrates)).
    """

    name: str
    arguments: list[Term]

    def __str__(self) -> str:
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"{self.name}({args_str})"

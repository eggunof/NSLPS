from dataclasses import dataclass
from typing import Self


@dataclass
class FormalStatement:
    """
    Represents a formal statement.
    """

    expression: str = ""

    @classmethod
    def parse(cls, statement: str) -> Self:
        """
        Parses a formal statement.

        :param statement: Statement to parse
        :return: Parsed formal statement
        """
        return cls(expression=statement.strip())

    def __str__(self):
        return self.expression

    def __repr__(self):
        return f"FormalStatement('{self.expression}')"

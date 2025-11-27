import logging
import re

from nslps.formal_language.fundamentals import Clause, Literal, Predicate, Term
from nslps.formal_language.parsing.formula_parser_exception import FormulaParserException

logger = logging.getLogger(__name__)


class FormulaParser:
    """
    Parses the raw string output from the LLM (Module 1) into structured
    Predicate Logic objects (Clauses, Literals, Predicates).
    """

    @staticmethod
    def parse_clause(statement: str) -> Clause:
        """
        Parses a raw string of comma-separated logical statements into a list of Clauses.
        Handles both unit clauses (facts) and complex clauses (rules using ∨).
        Example input: "Human(Socrates), ¬Human(x) ∨ Mortal(x)"
        """

        if not statement:
            raise FormulaParserException("Empty statement provided for parsing.")

        literal_strs = [l.strip() for l in statement.split("∨")]

        literals: list[Literal] = []
        for literal_str in literal_strs:
            try:
                literals.append(FormulaParser._parse_literal_string(literal_str))
            except FormulaParserException as e:
                logger.error(
                    "Parsing error for literal '%s' in statement '%s': %s",
                    literal_str,
                    statement,
                    e,
                )
                raise

        return Clause(literals)

    @staticmethod
    def _parse_literal_string(literal_str: str) -> Literal:
        """Parses a single literal string, e.g., '¬Mortal(x)' or 'Human(Socrates)'."""

        is_negated = literal_str.startswith("¬")
        if is_negated:
            literal_str = literal_str[1:]

        # Find predicate name and arguments within parentheses
        match = re.match(r"([A-Za-zА-Яа-я_]+)\((.*)\)", literal_str)
        if not match:
            raise FormulaParserException(f"Invalid predicate format: {literal_str}")

        predicate_name = match.group(1)
        args_str = match.group(2).strip()

        arguments: list[Term] = []
        if args_str:
            for arg_name in [a.strip() for a in args_str.split(",")]:
                if arg_name:
                    arguments.append(FormulaParser._parse_term(arg_name))

        predicate = Predicate(predicate_name, arguments)
        return Literal(predicate, is_negated)

    @staticmethod
    def _parse_term(term_str: str) -> Term:
        """Determines if a string is a variable or a constant."""
        # Simple rule: if starts with lowercase letter, it's a variable (e.g., 'x').
        # Otherwise, it's a constant (e.g., 'Socrates').
        is_variable = term_str.islower() and term_str.isalpha()
        return Term(term_str, is_variable)

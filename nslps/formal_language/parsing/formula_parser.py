import re

from nslps.formal_language.fundamentals import Clause, Literal, Predicate, Term
from nslps.formal_language.parsing.formula_parser_exception import FormulaParserException


class FormulaParser:
    """
    Parses the raw string output from the LLM (Module 1) into structured
    Predicate Logic objects (Clauses, Literals, Predicates).
    """

    @staticmethod
    def parse_clauses_from_raw_string(statements: list[str]) -> list[Clause]:
        """
        Parses a raw string of comma-separated logical statements into a list of Clauses.
        Handles both unit clauses (facts) and complex clauses (rules using ∨).
        Example input: "Human(Socrates), ¬Human(x) ∨ Mortal(x)"
        """
        clauses: list[Clause] = []

        # Split by comma to get individual statements (which might be complex clauses)
        for statement in statements:
            if not statement:
                continue

            # If the statement contains '∨', it's a non-unit clause (rule)
            if "∨" in statement:
                literal_strs = [l.strip() for l in statement.split("∨")]
            else:
                # Otherwise, it's a unit clause (fact or goal)
                literal_strs = [statement]

            literals: list[Literal] = []
            for lit_str in literal_strs:
                try:
                    literals.append(FormulaParser._parse_literal_string(lit_str))
                except FormulaParserException as e:
                    print(f"Parsing error for literal '{lit_str}': {e}")
                    continue

            if literals:
                clauses.append(Clause(literals))

        return clauses

    @staticmethod
    def _parse_term(term_str: str) -> Term:
        """Determines if a string is a variable or a constant."""
        # Simple rule: if starts with lowercase letter, it's a variable (e.g., 'x').
        # Otherwise, it's a constant (e.g., 'Socrates').
        is_variable = term_str.islower() and term_str.isalpha()
        return Term(term_str, is_variable)

    @staticmethod
    def _parse_literal_string(literal_str: str) -> Literal:
        """Parses a single literal string, e.g., '¬Mortal(x)' or 'Human(Socrates)'."""

        is_negated = literal_str.startswith("¬")
        if is_negated:
            literal_str = literal_str[1:]

        # Find predicate name and arguments within parentheses
        match = re.match(r"([A-Za-z]+)\((.*)\)", literal_str)
        if not match:
            raise FormulaParserException(f"Invalid predicate format: {literal_str}")

        predicate_name = match.group(1)
        args_str = match.group(2).strip()

        arguments: list[Term] = []
        if args_str:
            # Arguments are comma-separated
            for arg_name in [a.strip() for a in args_str.split(",")]:
                if arg_name:
                    arguments.append(FormulaParser._parse_term(arg_name))

        predicate = Predicate(predicate_name, arguments)
        return Literal(predicate, is_negated)

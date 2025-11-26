import pytest

from nslps.formal_language.fundamentals import Clause, Literal, Predicate, Term
from nslps.formal_language.proofing import ResolutionEngine


@pytest.fixture
def engine() -> ResolutionEngine:
    return ResolutionEngine()


def test_simple_modus_ponens(engine: ResolutionEngine) -> None:
    """
    Test:
    1. Man(Socrates)
    2. Man(x) -> Mortal(x)  <=> ¬Man(x) ∨ Mortal(x)
    Goal: Mortal(Socrates)
    """
    # Terms
    socrates = Term("Socrates", is_variable=False)
    x = Term("x", is_variable=True)

    # Predicates
    man_soc = Predicate("Man", [socrates])
    man_x = Predicate("Man", [x])
    mortal_x = Predicate("Mortal", [x])
    mortal_soc = Predicate("Mortal", [socrates])

    # Clauses
    # Fact: Man(Socrates)
    c1 = Clause([Literal(man_soc)])
    # Rule: ¬Man(x) ∨ Mortal(x)
    c2 = Clause([Literal(man_x, is_negated=True), Literal(mortal_x)])

    kb = [c1, c2]

    # Goal: Mortal(Socrates)
    # The engine will negate this to ¬Mortal(Socrates) and look for contradiction
    goal = Clause([Literal(mortal_soc)])

    result = engine.solve(kb, goal)

    assert result.is_proven
    assert any("Contradiction" in step.description for step in result.proof_log)


def test_unification_failure(engine: ResolutionEngine) -> None:
    """
    Test that resolution fails if terms don't match.
    Fact: Man(Plato)
    Rule: Man(Socrates) -> Mortal(Socrates)
    Goal: Mortal(Plato)
    """
    plato = Term("Plato", False)
    socrates = Term("Socrates", False)

    c1 = Clause([Literal(Predicate("Man", [plato]))])
    c2 = Clause(
        [
            Literal(Predicate("Man", [socrates]), is_negated=True),
            Literal(Predicate("Mortal", [socrates])),
        ]
    )

    kb = [c1, c2]
    goal = Clause([Literal(Predicate("Mortal", [plato]))])

    result = engine.solve(kb, goal)
    assert not result.is_proven

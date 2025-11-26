from nslps.formal_language.fundamentals import Clause, Literal, Predicate, Term
from nslps.formal_language.proofing.proof_step import ProofStep
from nslps.formal_language.proofing.resolution_result import ResolutionResult
from nslps.formal_language.proofing.unification_exception import UnificationException


class ResolutionEngine:
    """
    Symbolic core of the system.
    Implements First-Order Logic resolution with unification.
    """

    def solve(self, knowledge_base: list[Clause], goal: Clause) -> ResolutionResult:
        """
        Attempts to prove the goal by refutation (Reductio ad absurdum).
        Adds the negation of the goal to KB and tries to derive an empty clause.
        """
        # Negate goal: Since goal is usually a single literal query like Mortal(Socrates),
        # its negation acts as the initial premise to be contradicted.
        # Note: A proper CNF conversion of a complex negated goal is out of scope
        # for this snippet, assuming goal is atomic.
        negated_goal_literals = [l.negation for l in goal.literals]

        # Each literal in negated goal becomes a separate unit clause
        clauses = list(knowledge_base)
        proof_log: list[ProofStep] = []

        # Initial population of proof log
        for i, c in enumerate(clauses):
            proof_log.append(ProofStep(i, f"Axiom: {c}", c))

        start_idx = len(clauses)
        for i, l in enumerate(negated_goal_literals):
            c = Clause([l])
            clauses.append(c)
            proof_log.append(ProofStep(start_idx + i, f"Negated Goal: {c}", c))

        new_clauses_generated = True
        step_counter = len(clauses)

        while new_clauses_generated:
            new_clauses_generated = False
            n = len(clauses)

            # Try to resolve every pair of clauses
            for i in range(n):
                for j in range(i + 1, n):
                    c1 = clauses[i]
                    c2 = clauses[j]

                    resolvents = self._resolve(c1, c2)

                    for res in resolvents:
                        # Check if empty clause (Contradiction found)
                        if not res.literals:
                            proof_log.append(
                                ProofStep(
                                    step_counter, "Contradiction found (Empty Clause)", res, [i, j]
                                )
                            )
                            return ResolutionResult(is_proven=True, proof_log=proof_log)

                        # Check redundancy (simplified)
                        if not self._is_redundant(res, clauses):
                            clauses.append(res)
                            proof_log.append(
                                ProofStep(
                                    step_counter, f"Resolution between {i} and {j}", res, [i, j]
                                )
                            )
                            step_counter += 1
                            new_clauses_generated = True

        return ResolutionResult(is_proven=False, proof_log=proof_log)

    def _resolve(self, c1: Clause, c2: Clause) -> list[Clause]:
        """Returns all possible resolvents between two clauses."""
        resolvents = []
        for l1 in c1.literals:
            for l2 in c2.literals:
                # Look for complementary pairs (P vs ¬P)
                if l1.predicate.name == l2.predicate.name and l1.is_negated != l2.is_negated:
                    try:
                        substitution = self._unify(l1.predicate, l2.predicate)
                        # Perform resolution step
                        new_literals = [
                                           self._apply_sub(l, substitution) for l in c1.literals if l != l1
                                       ] + [self._apply_sub(l, substitution) for l in c2.literals if l != l2]
                        # Remove duplicates
                        unique_literals = []
                        seen = set()
                        for l in new_literals:
                            s = str(l)
                            if s not in seen:
                                seen.add(s)
                                unique_literals.append(l)

                        resolvents.append(Clause(unique_literals))
                    except UnificationException:
                        continue
        return resolvents

    def _unify(self, p1: Predicate, p2: Predicate) -> dict[str, Term]:
        """Standard unification algorithm for two predicates."""
        if p1.name != p2.name or len(p1.arguments) != len(p2.arguments):
            raise UnificationException()

        substitution: dict[str, Term] = {}
        for arg1, arg2 in zip(p1.arguments, p2.arguments):
            self._unify_terms(arg1, arg2, substitution)

        return substitution

    def _unify_terms(self, t1: Term, t2: Term, subst: dict[str, Term]) -> None:
        if t1 == t2:
            return
        if t1.is_variable:
            self._add_substitution(t1.name, t2, subst)
        elif t2.is_variable:
            self._add_substitution(t2.name, t1, subst)
        else:
            raise UnificationException("Constants do not match")

    @staticmethod
    def _add_substitution(var_name: str, term: Term, subst: dict[str, Term]) -> None:
        if var_name in subst:
            if subst[var_name] != term:
                raise UnificationException("Variable conflict")
        subst[var_name] = term

    @staticmethod
    def _apply_sub(literal: Literal, subst: dict[str, Term]) -> Literal:
        """Applies substitution to a literal."""
        new_args = []
        for arg in literal.predicate.arguments:
            if arg.is_variable and arg.name in subst:
                new_args.append(subst[arg.name])
            else:
                new_args.append(arg)

        return Literal(Predicate(literal.predicate.name, new_args), literal.is_negated)

    @staticmethod
    def _is_redundant(new_clause: Clause, existing_clauses: list[Clause]) -> bool:
        """Simple redundancy check based on string representation."""
        s = str(new_clause)
        return any(str(c) == s for c in existing_clauses)

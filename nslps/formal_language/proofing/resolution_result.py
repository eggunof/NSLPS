from dataclasses import dataclass

from nslps.formal_language.proofing.proof_step import ProofStep


@dataclass
class ResolutionResult:
    """The outcome of the resolution process."""

    is_proven: bool
    proof_log: list[ProofStep]

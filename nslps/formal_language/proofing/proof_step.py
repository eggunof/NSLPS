from dataclasses import dataclass, field
from typing import Optional

from nslps.formal_language.fundamentals import Clause


@dataclass
class ProofStep:
    """Captures a single step in the resolution proof for explanation."""

    step_id: int
    description: str
    clause_produced: Optional[Clause] = None
    parents: list[int] = field(default_factory=list)

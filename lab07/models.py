from dataclasses import dataclass
from functools import total_ordering
from typing import Any


@total_ordering
@dataclass(frozen=True, eq=False)
class LabResult:
    student: str
    lab: str
    score: float
    attempts: int
    submitted: bool

    def klyuch(self) -> tuple[float, int, str, str]:
        return (self.score, self.attempts, self.student, self.lab)

    def __eq__(self, inshyi: Any) -> bool:
        if not isinstance(inshyi, LabResult):
            return NotImplemented
        return self.klyuch() == inshyi.klyuch()

    def __lt__(self, inshyi: Any) -> bool:
        if not isinstance(inshyi, LabResult):
            return NotImplemented
        return self.klyuch() < inshyi.klyuch()

    def __hash__(self) -> int:
        return hash(self.klyuch())

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

    def sort_key(self) -> tuple[float, int, str, str]:
        return (self.score, self.attempts, self.student, self.lab)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, LabResult):
            return NotImplemented
        return self.sort_key() == other.sort_key()

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, LabResult):
            return NotImplemented
        return self.sort_key() < other.sort_key()

    def __hash__(self) -> int:
        return hash(self.sort_key())

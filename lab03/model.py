from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Literal, Mapping

Status = Literal["todo", "in_progress", "done"]


def make_metadata(**data: str) -> Mapping[str, str]:
    copy_ = dict(data)
    return MappingProxyType(copy_)


@dataclass(frozen=True, slots=True)
class Comment:
    author: str
    text: str


@dataclass(frozen=True, slots=True)
class Task:
    id: int
    title: str
    status: Status
    priority: int
    comments: tuple[Comment, ...]
    labels: frozenset[str]
    metadata: Mapping[str, str] = field(hash=False)

    def comments_count(self) -> int:
        return len(self.comments)

    def with_comment(self, comment: Comment) -> "Task":
        return replace(self, comments=self.comments + (comment,))

    def add_label(self, label: str) -> "Task":
        return replace(self, labels=self.labels | frozenset({label}))

    def with_status(self, status: Status) -> "Task":
        return replace(self, status=status)

    def with_priority(self, priority: int) -> "Task":
        if not 1 <= priority <= 5:
            raise ValueError("priorytet maye buty vid 1 do 5")
        return replace(self, priority=priority)

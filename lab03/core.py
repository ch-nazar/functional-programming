from collections.abc import Mapping
from dataclasses import replace
from types import MappingProxyType
from typing import Any

from model import Comment, Status, Task, make_metadata


def create_task(id: int, title: str, **metadata: str) -> Task:
    return Task(id, title, "todo", 3, (), frozenset(), make_metadata(**metadata))


def add_comment(task: Task, comment: Comment) -> Task:
    return replace(task, comments=task.comments + (comment,))


def add_label(task: Task, label: str) -> Task:
    return replace(task, labels=task.labels | frozenset({label}))


def change_status(task: Task, status: Status) -> Task:
    return replace(task, status=status)


def change_priority(task: Task, priority: int) -> Task:
    if not 1 <= priority <= 5:
        raise ValueError("priorytet maye buty vid 1 do 5")
    return replace(task, priority=priority)


def update_metadata(task: Task, **new_values: str) -> Task:
    merged = {**task.metadata, **new_values}
    return replace(task, metadata=make_metadata(**merged))


def freeze(obj: Any) -> Any:
    if isinstance(obj, Mapping):
        return MappingProxyType({key: freeze(value) for key, value in obj.items()})
    if isinstance(obj, set):
        return frozenset(freeze(item) for item in obj)
    if isinstance(obj, (list, tuple)):
        return tuple(freeze(item) for item in obj)
    return obj

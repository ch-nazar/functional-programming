from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol, TypeAlias

Value: TypeAlias = str | int | float | bool | None
Operator = Literal["==", "and", "or", "not"]


class HasName(Protocol):
    @property
    def name(self) -> str: ...


@dataclass(frozen=True)
class Field:
    name: str

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("nazva polya ne mozhe buty porozhnoyu")


@dataclass(frozen=True)
class Eq:
    field: Field
    value: Value


@dataclass(frozen=True)
class And:
    left: Query
    right: Query


@dataclass(frozen=True)
class Or:
    left: Query
    right: Query


@dataclass(frozen=True)
class Not:
    inner: Query


Query: TypeAlias = Field | Eq | And | Or | Not

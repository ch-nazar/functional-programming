from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol, TypeAlias

Znachennya: TypeAlias = str | int | float | bool | None
Operator = Literal["==", "and", "or", "not"]


class MaiePole(Protocol):
    @property
    def nazva(self) -> str: ...


@dataclass(frozen=True)
class Pole:
    nazva: str

    def __post_init__(self) -> None:
        if not self.nazva:
            raise ValueError("nazva polya ne mozhe buty porozhnoyu")


@dataclass(frozen=True)
class Rivno:
    pole: Pole
    znachennya: Znachennya


@dataclass(frozen=True)
class Ta:
    livyi: Query
    pravyi: Query


@dataclass(frozen=True)
class Abo:
    livyi: Query
    pravyi: Query


@dataclass(frozen=True)
class Ne:
    vnutrishnii: Query


Query: TypeAlias = Pole | Rivno | Ta | Abo | Ne

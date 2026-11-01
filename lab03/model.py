from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Literal, Mapping

Status = Literal["todo", "u_roboti", "zrobleno"]


def zrobyty_metadani(**dani: str) -> Mapping[str, str]:
    kopiya = dict(dani)
    return MappingProxyType(kopiya)


@dataclass(frozen=True, slots=True)
class Komentar:
    avtor: str
    tekst: str


@dataclass(frozen=True, slots=True)
class Zadacha:
    id: int
    nazva: str
    status: Status
    priorytet: int
    komentari: tuple[Komentar, ...]
    mitky: frozenset[str]
    metadani: Mapping[str, str] = field(hash=False)

    def kilkist_komentariv(self) -> int:
        return len(self.komentari)


def stvoryty_zadachu(id: int, nazva: str, **metadani: str) -> Zadacha:
    return Zadacha(id, nazva, "todo", 3, (), frozenset(), zrobyty_metadani(**metadani))


def dodaty_komentar(zadacha: Zadacha, komentar: Komentar) -> Zadacha:
    return replace(zadacha, komentari=zadacha.komentari + (komentar,))


def dodaty_mitku(zadacha: Zadacha, mitka: str) -> Zadacha:
    return replace(zadacha, mitky=zadacha.mitky | frozenset({mitka}))


def zminyty_status(zadacha: Zadacha, status: Status) -> Zadacha:
    return replace(zadacha, status=status)


def zminyty_priorytet(zadacha: Zadacha, priorytet: int) -> Zadacha:
    if not 1 <= priorytet <= 5:
        raise ValueError("priorytet maye buty vid 1 do 5")
    return replace(zadacha, priorytet=priorytet)


def zminyty_metadani(zadacha: Zadacha, **novi: str) -> Zadacha:
    zlyti = {**zadacha.metadani, **novi}
    return replace(zadacha, metadani=zrobyty_metadani(**zlyti))

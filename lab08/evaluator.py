from typing import Any, Mapping, Sequence, assert_never

from model import Abo, MaiePole, Ne, Pole, Query, Rivno, Ta


def obchyslyty_zapyt(zapyt: Query, rekord: Mapping[str, Any]) -> bool:
    match zapyt:
        case Pole(nazva):
            return bool(rekord.get(nazva, False))
        case Rivno(pole, znachennya):
            return pole.nazva in rekord and rekord[pole.nazva] == znachennya
        case Ta(livyi, pravyi):
            return obchyslyty_zapyt(livyi, rekord) and obchyslyty_zapyt(pravyi, rekord)
        case Abo(livyi, pravyi):
            return obchyslyty_zapyt(livyi, rekord) or obchyslyty_zapyt(pravyi, rekord)
        case Ne(vnutrishnii):
            return not obchyslyty_zapyt(vnutrishnii, rekord)
        case _:
            assert_never(zapyt)


def vidfiltruvaty(zapyt: Query, rekordy: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return [rekord for rekord in rekordy if obchyslyty_zapyt(zapyt, rekord)]


def nazva_polya(obyekt: MaiePole) -> str:
    return obyekt.nazva


def polya_zapytu(zapyt: Query) -> frozenset[str]:
    match zapyt:
        case Pole():
            return frozenset({nazva_polya(zapyt)})
        case Rivno(pole, _):
            return frozenset({nazva_polya(pole)})
        case Ta(livyi, pravyi) | Abo(livyi, pravyi):
            return polya_zapytu(livyi) | polya_zapytu(pravyi)
        case Ne(vnutrishnii):
            return polya_zapytu(vnutrishnii)
        case _:
            assert_never(zapyt)

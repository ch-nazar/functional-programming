from typing import assert_never

from model import Abo, Ne, Operator, Pole, Query, Rivno, Ta

ZNAKY: dict[Operator, str] = {"==": "==", "and": "and", "or": "or", "not": "not"}


def renderyty_zapyt(zapyt: Query) -> str:
    match zapyt:
        case Pole(nazva):
            return nazva
        case Rivno(pole, znachennya):
            return f"{pole.nazva} {ZNAKY['==']} {znachennya!r}"
        case Ta(livyi, pravyi):
            return f"({renderyty_zapyt(livyi)} {ZNAKY['and']} {renderyty_zapyt(pravyi)})"
        case Abo(livyi, pravyi):
            return f"({renderyty_zapyt(livyi)} {ZNAKY['or']} {renderyty_zapyt(pravyi)})"
        case Ne(vnutrishnii):
            return f"{ZNAKY['not']} {renderyty_zapyt(vnutrishnii)}"
        case _:
            assert_never(zapyt)

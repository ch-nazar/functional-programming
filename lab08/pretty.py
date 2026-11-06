from typing import assert_never

from model import Or, Not, Operator, Field, Query, Eq, And

SYMBOLS: dict[Operator, str] = {"==": "==", "and": "and", "or": "or", "not": "not"}


def render_query(query: Query) -> str:
    match query:
        case Field(name):
            return name
        case Eq(field, value):
            return f"{field.name} {SYMBOLS['==']} {value!r}"
        case And(left, right):
            return f"({render_query(left)} {SYMBOLS['and']} {render_query(right)})"
        case Or(left, right):
            return f"({render_query(left)} {SYMBOLS['or']} {render_query(right)})"
        case Not(inner):
            return f"{SYMBOLS['not']} {render_query(inner)}"
        case _:
            assert_never(query)

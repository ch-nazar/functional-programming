# Lab 8, variant 15: abstraktne derevo zapytiv

ADT: Pole, Rivno, Ta, Abo, Ne (frozen dataclass), Query = TypeAlias dlya ob'yednannya.
Literal: Operator. Protocol: MaiePole. Operatsiyi: obchyslyty_zapyt (eval_query), renderyty_zapyt (render_query),
polya_zapytu, vidfiltruvaty. Rozbir cherez match/case, usi vitky zakryti assert_never.
Vidsutnie pole v zapysi daye False (ne pomylku).

Zapusk: python main.py | pytest -q | mypy --strict .

from evaluator import obchyslyty_zapyt, polya_zapytu, vidfiltruvaty
from model import Abo, Ne, Pole, Rivno, Ta
from pretty import renderyty_zapyt

REKORDY = [
    {"nazva": "Zadacha 1", "status": "open", "priorytet": 1, "terminova": True},
    {"nazva": "Zadacha 2", "status": "closed", "priorytet": 2, "terminova": False},
    {"nazva": "Zadacha 3", "status": "open", "priorytet": 3, "terminova": False},
]

if __name__ == "__main__":
    zapyt = Ta(Rivno(Pole("status"), "open"), Abo(Pole("terminova"), Ne(Rivno(Pole("priorytet"), 3))))
    print("Zapyt:", renderyty_zapyt(zapyt))
    print("Polya:", sorted(polya_zapytu(zapyt)))
    for rekord in REKORDY:
        print(rekord["nazva"], "->", obchyslyty_zapyt(zapyt, rekord))
    print("Pidkhodyat:", [rekord["nazva"] for rekord in vidfiltruvaty(zapyt, REKORDY)])

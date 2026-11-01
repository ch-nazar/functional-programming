from timeit import timeit

from model import Komentar, dodaty_komentar, dodaty_mitku, stvoryty_zadachu, zminyty_status

KILKIST = 2000


def zminna_versiya() -> dict:
    zadacha = {"komentari": [], "mitky": set(), "status": "todo"}
    for nomer in range(KILKIST):
        zadacha["komentari"].append(("avtor", str(nomer)))
        zadacha["mitky"].add(f"mitka{nomer % 50}")
        zadacha["status"] = "u_roboti"
    return zadacha


def nezminna_versiya():
    zadacha = stvoryty_zadachu(1, "test")
    for nomer in range(KILKIST):
        zadacha = dodaty_komentar(zadacha, Komentar("avtor", str(nomer)))
        zadacha = dodaty_mitku(zadacha, f"mitka{nomer % 50}")
        zadacha = zminyty_status(zadacha, "u_roboti")
    return zadacha


def vymiryaty(funktsiya) -> float:
    return timeit(funktsiya, number=5) / 5


if __name__ == "__main__":
    print(f"Zminna versiya (list/set/dict): {vymiryaty(zminna_versiya):.4f} s")
    print(f"Nezminna versiya (tuple/frozenset): {vymiryaty(nezminna_versiya):.4f} s")
    print("Vysnovok: nezminna versiya povilnisha na kopiyuvanni tuple, zate bezpechna i hashovana")

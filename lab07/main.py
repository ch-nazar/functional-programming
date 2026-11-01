from pathlib import Path

from core import obrobyty, zahalnyi_bal


def pokazaty(nazva: str, rezultaty) -> None:
    print(f"\n{nazva}:")
    for misce, rezultat in enumerate(rezultaty, start=1):
        print(f"{misce}. {rezultat.student} {rezultat.lab} bal={rezultat.score} sprob={rezultat.attempts}")
    print("Zahalnyi bal:", zahalnyi_bal(rezultaty))


if __name__ == "__main__":
    papka = Path(__file__).parent
    pokazaty("Top-3 z JSON-fajlu", obrobyty(papka / "sample_data.json", 3))
    pokazaty("Top-3 z CSV-fajlu", obrobyty(papka / "sample_data.csv", 3))
    with open(papka / "sample_data.csv", encoding="utf-8") as fajl:
        pokazaty("Top-2 z vidkrytoho fajlu", obrobyty(fajl, 2))

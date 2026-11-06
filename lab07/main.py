from pathlib import Path

from core import process, total_score


def show(title: str, results) -> None:
    print(f"\n{title}:")
    for place, result in enumerate(results, start=1):
        print(f"{place}. {result.student} {result.lab} bal={result.score} sprob={result.attempts}")
    print("Zahalnyi bal:", total_score(results))


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    show("Top-3 z JSON-fajlu", process(base_dir / "sample_data.json", 3))
    show("Top-3 z CSV-fajlu", process(base_dir / "sample_data.csv", 3))
    with open(base_dir / "sample_data.csv", encoding="utf-8") as file:
        show("Top-2 z vidkrytoho fajlu", process(file, 2))

from timeit import timeit

from model import Comment
from core import add_comment, add_label, create_task, change_status

COUNT = 2000


def mutable_version() -> dict:
    task = {"komentari": [], "mitky": set(), "status": "todo"}
    for index in range(COUNT):
        task["komentari"].append(("avtor", str(index)))
        task["mitky"].add(f"mitka{index % 50}")
        task["status"] = "in_progress"
    return task


def immutable_version():
    task = create_task(1, "test")
    for index in range(COUNT):
        task = add_comment(task, Comment("avtor", str(index)))
        task = add_label(task, f"mitka{index % 50}")
        task = change_status(task, "in_progress")
    return task


def measure(func) -> float:
    return timeit(func, number=5) / 5


if __name__ == "__main__":
    print(f"Zminna versiya (list/set/dict): {measure(mutable_version):.4f} s")
    print(f"Nezminna versiya (tuple/frozenset): {measure(immutable_version):.4f} s")
    print("Vysnovok: nezminna versiya povilnisha na kopiyuvanni tuple, zate bezpechna i hashovana")

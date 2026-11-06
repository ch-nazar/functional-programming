from timeit import timeit

from core import add_comment, create_task
from model import Comment


def mutable_updates(count: int) -> list:
    comments: list = []
    for index in range(count):
        comments.append(("author", str(index)))
    return comments


def immutable_updates(count: int):
    task = create_task(1, "perf")
    for index in range(count):
        task = add_comment(task, Comment("author", str(index)))
    return task


def test_performance_report():
    mutable_time = timeit(lambda: mutable_updates(500), number=3)
    immutable_time = timeit(lambda: immutable_updates(500), number=3)
    print(f"mutable={mutable_time:.4f}s immutable={immutable_time:.4f}s")
    assert mutable_time >= 0 and immutable_time >= 0


def test_immutable_result_is_correct():
    assert immutable_updates(100).comments_count() == 100

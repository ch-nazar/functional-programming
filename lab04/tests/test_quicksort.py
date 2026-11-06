import random

from algorithms import quicksort


def test_quicksort_basic():
    assert quicksort([]) == []
    assert quicksort([1]) == [1]
    assert quicksort([3, 2, 1]) == [1, 2, 3]
    assert quicksort([2, 2, 1, 3, 2]) == [1, 2, 2, 2, 3]


def test_quicksort_random():
    xs = [random.randint(-1000, 1000) for _ in range(1000)]
    assert quicksort(xs) == sorted(xs)


def test_quicksort_does_not_modify_input():
    xs = [3, 1, 2]
    quicksort(xs)
    assert xs == [3, 1, 2]

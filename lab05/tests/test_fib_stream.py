from itertools import islice

from streams import drop, fib_stream, naturals, take


def test_first_10():
    assert list(islice(fib_stream(), 10)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_naturals():
    assert take(3, naturals()) == [1, 2, 3]
    assert take(2, naturals(10)) == [10, 11]


def test_combine_take_and_drop():
    assert take(8, drop(5, fib_stream())) == [5, 8, 13, 21, 34, 55, 89, 144]

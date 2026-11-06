import pytest

from algorithms import fact, fib, fib_iter


def test_fib_small():
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert [fib(n) for n in range(10)] == expected


def test_fib_iter_matches():
    for n in range(50):
        assert fib(n) == fib_iter(n)


def test_cache_clear():
    fib.cache_clear()
    assert fib(0) == 0
    assert fib.cache_info().currsize >= 1


def test_fib_invalid_input():
    with pytest.raises(ValueError):
        fib(-1)
    with pytest.raises(ValueError):
        fib_iter(-5)


def test_fact():
    assert fact(5) == 120
    assert fact(0) == 1

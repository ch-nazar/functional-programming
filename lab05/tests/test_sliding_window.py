import pytest

from streams import moving_average, sliding_window


def test_windows_basic():
    assert list(sliding_window([1, 2, 3, 4], 3)) == [(1, 2, 3), (2, 3, 4)]


def test_window_sums():
    assert list(map(sum, sliding_window(range(5), 2))) == [1, 3, 5, 7]


def test_window_longer_than_input_is_empty():
    assert list(sliding_window([1, 2], 5)) == []


def test_invalid_window_size():
    with pytest.raises(ValueError):
        sliding_window([1, 2, 3], 0)


def test_moving_average_over_windows():
    assert list(moving_average([1, 2, 3, 4], 2)) == [1.5, 2.5, 3.5]

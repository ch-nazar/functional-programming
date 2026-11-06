import pytest

from streams import (valid_only, sliding_window, prefix_stats, drop,
                   moving_average, measurements, take)


def make_provider(value):
    source = iter(value)
    calls = {"count": 0}

    def provider():
        calls["count"] += 1
        return next(source, None)

    return provider, calls


def test_measurements_stops_on_sentinel():
    provider, _ = make_provider([1.0, 2.0, 3.0])
    assert list(measurements(provider)) == [1.0, 2.0, 3.0]


def test_empty_source():
    provider, _ = make_provider([])
    assert list(measurements(provider)) == []
    assert take(3, iter([])) == []


def test_valid_only_rejects_invalid():
    assert list(valid_only([5, -1, 20, 100, 0], 0, 50)) == [5, 20, 0]


def test_take_zero_and_more_than_available():
    assert take(0, iter([1, 2, 3])) == []
    assert take(10, iter([1, 2, 3])) == [1, 2, 3]


def test_drop():
    assert list(drop(2, iter([1, 2, 3, 4]))) == [3, 4]
    assert list(drop(0, iter([1, 2]))) == [1, 2]
    assert list(drop(5, iter([1, 2]))) == []


def test_sliding_window():
    assert list(sliding_window([1, 2, 3, 4], 2)) == [(1, 2), (2, 3), (3, 4)]
    assert list(sliding_window([1, 2, 3], 3)) == [(1, 2, 3)]


def test_window_longer_than_stream():
    assert list(sliding_window([1, 2], 5)) == []


def test_invalid_window_size():
    with pytest.raises(ValueError):
        sliding_window([1, 2, 3], 0)
    with pytest.raises(ValueError):
        moving_average([1, 2, 3], -2)


def test_moving_average():
    assert list(moving_average([1, 2, 3, 4], 2)) == [1.5, 2.5, 3.5]


def test_prefix_stats():
    result = list(prefix_stats([4, 2, 6]))
    assert result == [(1, 4, 4, 4, 4.0), (2, 6, 2, 4, 3.0), (3, 12, 2, 6, 4.0)]


def test_laziness_provider():
    provider, calls = make_provider([5, 100, 7, 8, 9, 10])
    stream = valid_only(measurements(provider), 0, 50)
    assert take(2, stream) == [5, 7]
    assert calls["count"] == 3


def test_laziness_moving_average():
    provider, calls = make_provider(range(1, 100))
    stream = moving_average(measurements(provider), 3)
    assert take(2, stream) == [2.0, 3.0]
    assert calls["count"] == 4


def test_laziness_prefix_stats():
    provider, calls = make_provider(range(1, 100))
    take(3, prefix_stats(measurements(provider)))
    assert calls["count"] == 3


def test_infinite_stream_not_hangs():
    provider = lambda: 1.0
    assert take(3, moving_average(measurements(provider), 2)) == [1.0, 1.0, 1.0]

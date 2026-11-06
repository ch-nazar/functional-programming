from collections import deque
from itertools import accumulate, count, islice, tee
from typing import Callable, Iterable, Iterator, Optional, TypeVar

T = TypeVar("T")


def measurements(provider: Callable[[], Optional[float]], sentinel: Optional[float] = None) -> Iterator[Optional[float]]:
    return iter(provider, sentinel)


def valid_only(stream: Iterable[float], lower_bound: float, upper_bound: float) -> Iterator[float]:
    return (value for value in stream if lower_bound <= value <= upper_bound)


def take(n: int, stream: Iterable[T]) -> list[T]:
    return list(islice(stream, n))


def drop(n: int, stream: Iterable[T]) -> Iterator[T]:
    return islice(stream, n, None)


def sliding_window(stream: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    if size <= 0:
        raise ValueError("rozmir vikna maye buty bilshe nulya")
    return build_windows(iter(stream), size)


def build_windows(source: Iterator[T], size: int) -> Iterator[tuple[T, ...]]:
    window: deque[T] = deque(islice(source, size), maxlen=size)
    if len(window) < size:
        return
    yield tuple(window)
    for value in source:
        window.append(value)
        yield tuple(window)


def moving_average(stream: Iterable[float], size: int) -> Iterator[float]:
    return (sum(window) / size for window in sliding_window(stream, size))


def prefix_stats(stream: Iterable[float]) -> Iterator[tuple[int, float, float, float, float]]:
    copy_for_total, copy_for_min, copy_for_max = tee(stream, 3)
    totals = accumulate(copy_for_total)
    minimums = accumulate(copy_for_min, min)
    maximums = accumulate(copy_for_max, max)
    for amount, total, minimum, maximum in zip(count(1), totals, minimums, maximums):
        yield amount, total, minimum, maximum, total / amount


def fib_stream() -> Iterator[int]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def naturals(start: int = 1) -> Iterator[int]:
    yield from count(start)

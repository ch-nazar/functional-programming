from collections import deque
from itertools import accumulate, count, islice, tee
from typing import Callable, Iterable, Iterator, Optional, TypeVar

T = TypeVar("T")


def vymiryuvannya(postachalnyk: Callable[[], Optional[float]], storozha: Optional[float] = None) -> Iterator[Optional[float]]:
    return iter(postachalnyk, storozha)


def dopustymi(potik: Iterable[float], nyzhnya_mezha: float, verkhnya_mezha: float) -> Iterator[float]:
    return (znachennya for znachennya in potik if nyzhnya_mezha <= znachennya <= verkhnya_mezha)


def vzyaty(n: int, potik: Iterable[T]) -> list[T]:
    return list(islice(potik, n))


def propustyty(n: int, potik: Iterable[T]) -> Iterator[T]:
    return islice(potik, n, None)


def kovzne_vikno(potik: Iterable[T], rozmir: int) -> Iterator[tuple[T, ...]]:
    if rozmir <= 0:
        raise ValueError("rozmir vikna maye buty bilshe nulya")
    return stvoryty_vikna(iter(potik), rozmir)


def stvoryty_vikna(dzherelo: Iterator[T], rozmir: int) -> Iterator[tuple[T, ...]]:
    vikno: deque[T] = deque(islice(dzherelo, rozmir), maxlen=rozmir)
    if len(vikno) < rozmir:
        return
    yield tuple(vikno)
    for znachennya in dzherelo:
        vikno.append(znachennya)
        yield tuple(vikno)


def ruhome_serednye(potik: Iterable[float], rozmir: int) -> Iterator[float]:
    return (sum(vikno) / rozmir for vikno in kovzne_vikno(potik, rozmir))


def prefiksni_statystyky(potik: Iterable[float]) -> Iterator[tuple[int, float, float, float, float]]:
    kopiya_dlya_sumy, kopiya_dlya_minimumu, kopiya_dlya_maksimumu = tee(potik, 3)
    sumy = accumulate(kopiya_dlya_sumy)
    minimumy = accumulate(kopiya_dlya_minimumu, min)
    maksimumy = accumulate(kopiya_dlya_maksimumu, max)
    for kilkist, suma, minimum, maksimum in zip(count(1), sumy, minimumy, maksimumy):
        yield kilkist, suma, minimum, maksimum, suma / kilkist

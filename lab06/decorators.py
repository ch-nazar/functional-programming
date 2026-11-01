import functools
import time
from functools import reduce
from typing import Any, Callable, ParamSpec, TypeVar

from closures import pustyi_zapys

P = ParamSpec("P")
R = TypeVar("R")
Dekorator = Callable[[Callable[P, R]], Callable[P, R]]


def vymiryany(hodynnyk: Callable[[], float] = time.perf_counter,
              zapys: Callable[[str], None] = pustyi_zapys) -> Dekorator:
    def dekorator(funktsiya: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(funktsiya)
        def obgortka(*args: P.args, **kwargs: P.kwargs) -> R:
            pochatok = hodynnyk()
            try:
                return funktsiya(*args, **kwargs)
            finally:
                zapys(f"{funktsiya.__name__} trvala {hodynnyk() - pochatok:.3f} s")

        return obgortka

    return dekorator


def povtory(sproby: int,
            vynyatky: tuple[type[BaseException], ...] = (Exception,),
            zatrymka: float = 0.0,
            spy: Callable[[float], None] = time.sleep,
            zapys: Callable[[str], None] = pustyi_zapys) -> Dekorator:
    if sproby <= 0:
        raise ValueError("sproby maye buty bilshe nulya")

    def dekorator(funktsiya: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(funktsiya)
        def obgortka(*args: P.args, **kwargs: P.kwargs) -> R:
            for nomer in range(1, sproby):
                try:
                    return funktsiya(*args, **kwargs)
                except vynyatky as pomylka:
                    zapys(f"sproba {nomer} z {sproby} ne vdalas: {pomylka}")
                    spy(zatrymka)
            return funktsiya(*args, **kwargs)

        return obgortka

    return dekorator


def keshovanyi(ttl: float,
               hodynnyk: Callable[[], float] = time.monotonic,
               zapys: Callable[[str], None] = pustyi_zapys) -> Dekorator:
    def dekorator(funktsiya: Callable[P, R]) -> Callable[P, R]:
        zberezheni: dict[Any, tuple[R, float]] = {}
        lichylnyky = {"vluchannya": 0, "promakhy": 0}

        @functools.wraps(funktsiya)
        def obgortka(*args: P.args, **kwargs: P.kwargs) -> R:
            klyuch = (args, tuple(sorted(kwargs.items())))
            if klyuch in zberezheni:
                znachennya, moment = zberezheni[klyuch]
                if hodynnyk() - moment < ttl:
                    lichylnyky["vluchannya"] += 1
                    zapys(f"kesh: vluchannya dlya {klyuch}")
                    return znachennya
                del zberezheni[klyuch]
            lichylnyky["promakhy"] += 1
            zapys(f"kesh: promakh dlya {klyuch}")
            rezultat = funktsiya(*args, **kwargs)
            zberezheni[klyuch] = (rezultat, hodynnyk())
            return rezultat

        setattr(obgortka, "cache_clear", zberezheni.clear)
        setattr(obgortka, "cache_info", lambda: dict(lichylnyky, rozmir=len(zberezheni)))
        return obgortka

    return dekorator


def skladaty(*dekoratory: Dekorator) -> Dekorator:
    def dekorator(funktsiya: Callable[P, R]) -> Callable[P, R]:
        return reduce(lambda poperednya, d: d(poperednya), reversed(dekoratory), funktsiya)

    return dekorator

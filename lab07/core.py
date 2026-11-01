from dataclasses import replace
from functools import partial, reduce
from itertools import islice
from operator import add, attrgetter, itemgetter, methodcaller
from typing import Any, Callable, Iterable

from loaders import Zapys, zavantazhyty_zapysy
from models import LabResult

TAK = frozenset({"true", "yes", "1", "tak", "так"})
dostaty_studenta = itemgetter("student")
dostaty_lab = itemgetter("lab")
dostaty_bal = itemgetter("score")
dostaty_sprobu = itemgetter("attempts")
dostaty_zdano = itemgetter("submitted")
prybraty_probily = methodcaller("strip")


def pipeline(znachennya: Any, *funktsiyi: Callable[[Any], Any]) -> Any:
    return reduce(lambda poperedne, funktsiya: funktsiya(poperedne), funktsiyi, znachennya)


def rozibraty_zdano(znachennya: Any) -> bool:
    return str(znachennya).strip().lower() in TAK


def normalizuvaty_zapys(zapys: Zapys) -> Zapys:
    return {
        "student": prybraty_probily(str(dostaty_studenta(zapys))).title(),
        "lab": prybraty_probily(str(dostaty_lab(zapys))).upper(),
        "score": float(dostaty_bal(zapys)),
        "attempts": int(dostaty_sprobu(zapys)),
        "submitted": rozibraty_zdano(dostaty_zdano(zapys)),
    }


def stvoryty_rezultat(zapys: Zapys) -> LabResult:
    return LabResult(**zapys)


def pidsumkovyi_bal(shtraf_za_sprobu: float, maksymum: float, rezultat: LabResult) -> LabResult:
    shtraf = shtraf_za_sprobu * max(rezultat.attempts - 1, 0)
    return replace(rezultat, score=max(min(rezultat.score, maksymum) - shtraf, 0.0))


def bahatokryterialne_sortuvannya(rezultaty: Iterable[LabResult]) -> list[LabResult]:
    za_imenem = sorted(rezultaty, key=attrgetter("student"))
    za_sprobamy = sorted(za_imenem, key=attrgetter("attempts"))
    return sorted(za_sprobamy, key=attrgetter("score"), reverse=True)


def top_n(n: int, rezultaty: Iterable[LabResult]) -> list[LabResult]:
    return list(islice(bahatokryterialne_sortuvannya(rezultaty), max(n, 0)))


def zahalnyi_bal(rezultaty: Iterable[LabResult]) -> float:
    return reduce(add, map(attrgetter("score"), rezultaty), 0.0)


def pobuduvaty_konveyer(n: int, shtraf_za_sprobu: float = 2.0, maksymum: float = 100.0) -> list[Callable[[Any], Any]]:
    return [
        partial(map, normalizuvaty_zapys),
        partial(filter, dostaty_zdano),
        partial(map, stvoryty_rezultat),
        partial(map, partial(pidsumkovyi_bal, shtraf_za_sprobu, maksymum)),
        partial(top_n, n),
    ]


def obrobyty(dzherelo: Any, n: int, shtraf_za_sprobu: float = 2.0, maksymum: float = 100.0) -> list[LabResult]:
    return pipeline(zavantazhyty_zapysy(dzherelo), *pobuduvaty_konveyer(n, shtraf_za_sprobu, maksymum))

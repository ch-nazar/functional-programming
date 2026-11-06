from dataclasses import replace
from functools import partial, reduce
from itertools import islice
from operator import add, attrgetter, itemgetter, methodcaller
from typing import Any, Callable, Iterable

from loaders import Record, load_records
from models import LabResult

TRUTHY = frozenset({"true", "yes", "1", "tak", "так"})
get_student = itemgetter("student")
get_lab = itemgetter("lab")
get_score = itemgetter("score")
get_attempts = itemgetter("attempts")
get_submitted = itemgetter("submitted")
strip_spaces = methodcaller("strip")


def pipeline(value: Any, *funcs: Callable[[Any], Any]) -> Any:
    return reduce(lambda previous, func: func(previous), funcs, value)


def parse_submitted(value: Any) -> bool:
    return str(value).strip().lower() in TRUTHY


def normalize_record(record: Record) -> Record:
    return {
        "student": strip_spaces(str(get_student(record))).title(),
        "lab": strip_spaces(str(get_lab(record))).upper(),
        "score": float(get_score(record)),
        "attempts": int(get_attempts(record)),
        "submitted": parse_submitted(get_submitted(record)),
    }


def make_result(record: Record) -> LabResult:
    return LabResult(**record)


def final_score(attempt_penalty: float, max_score: float, result: LabResult) -> LabResult:
    penalty = attempt_penalty * max(result.attempts - 1, 0)
    return replace(result, score=max(min(result.score, max_score) - penalty, 0.0))


def multi_key_sort(results: Iterable[LabResult]) -> list[LabResult]:
    by_name = sorted(results, key=attrgetter("student"))
    by_attempts = sorted(by_name, key=attrgetter("attempts"))
    return sorted(by_attempts, key=attrgetter("score"), reverse=True)


def top_n(n: int, results: Iterable[LabResult]) -> list[LabResult]:
    return list(islice(multi_key_sort(results), max(n, 0)))


def total_score(results: Iterable[LabResult]) -> float:
    return reduce(add, map(attrgetter("score"), results), 0.0)


def build_pipeline(n: int, attempt_penalty: float = 2.0, max_score: float = 100.0) -> list[Callable[[Any], Any]]:
    return [
        partial(map, normalize_record),
        partial(filter, get_submitted),
        partial(map, make_result),
        partial(map, partial(final_score, attempt_penalty, max_score)),
        partial(top_n, n),
    ]


def process(source: Any, n: int, attempt_penalty: float = 2.0, max_score: float = 100.0) -> list[LabResult]:
    return pipeline(load_records(source), *build_pipeline(n, attempt_penalty, max_score))

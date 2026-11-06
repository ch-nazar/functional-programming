from closures import make_controlled_clock
from decorators import cached, compose, retries, timed
from service import make_flaky_service


def run(cache_outer: bool):
    clock, advance = make_controlled_clock()
    timing_logs: list[str] = []
    service, call_count = make_flaky_service(2)
    cache_decorator = cached(ttl=60.0, time_fn=clock)
    retry_decorator = retries(attempts=3, exceptions=(ConnectionError,), sleep=advance)
    timed_decorator = timed(logger=timing_logs.append, clock=clock)
    order = (cache_decorator, retry_decorator, timed_decorator) if cache_outer else (timed_decorator, cache_decorator, retry_decorator)
    wrapped = compose(*order)(service)
    first, second = wrapped(1), wrapped(1)
    return first, second, len(timing_logs), call_count()


def test_order_changes_number_of_timings():
    assert run(True) == ("profile_1", "profile_1", 3, 3)
    assert run(False) == ("profile_1", "profile_1", 2, 3)


def test_cache_hits_depend_on_order():
    clock, _ = make_controlled_clock()
    service, _ = make_flaky_service(2)
    wrapped = compose(retries(attempts=3, sleep=lambda s: None), cached(ttl=60.0, time_fn=clock))(service)
    wrapped(1)
    wrapped(1)
    info = wrapped.__wrapped__.cache_info()
    assert info["misses"] == 3
    assert info["hits"] == 1


def test_metadata_preserved_after_composition():
    service, _ = make_flaky_service(0)
    wrapped = compose(cached(), retries(), timed(logger=lambda m: None))(service)
    assert wrapped.__name__ == "get_profile"
    assert wrapped.__doc__ == service.__doc__
    assert wrapped.__wrapped__ is not None

from closures import make_controlled_clock, make_logger
from decorators import cached, compose, retries, timed
from service import make_flaky_service


def show_order(title: str, cache_outer: bool) -> None:
    print(f"\n=== {title} ===")
    clock, advance = make_controlled_clock()
    logger = make_logger("log")
    service, _ = make_flaky_service(failures=2)
    cache_decorator = cached(ttl=60, time_fn=clock, logger=logger)
    retry_decorator = retries(attempts=3, delay=0.5, sleep=advance, logger=logger)
    timed_decorator = timed("get_profile", unit="s", logger=logger, clock=clock)
    order = (cache_decorator, retry_decorator, timed_decorator) if cache_outer else (timed_decorator, cache_decorator, retry_decorator)
    wrapped = compose(*order)(service)
    print("Pershyi vyklyk:", wrapped(7))
    print("Drugyi vyklyk:", wrapped(7))


if __name__ == "__main__":
    show_order("Poryadok: cached -> retries -> timed (chas vymiryuye kozhnu sprobu)", True)
    show_order("Poryadok: timed -> cached -> retries (chas vymiryuye kozhen vyklyk)", False)

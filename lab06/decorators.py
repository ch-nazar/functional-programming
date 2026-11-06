import functools
import random
import threading
import time
from functools import reduce
from typing import Any, Callable, Hashable, Literal, ParamSpec, TypeVar

from closures import noop_logger

P = ParamSpec("P")
R = TypeVar("R")
Decorator = Callable[[Callable[P, R]], Callable[P, R]]


def timed(
    label: str | None = None,
    *,
    unit: Literal["s", "ms", "us"] = "ms",
    logger: Callable[[str], None] = print,
    clock: Callable[[], float] = time.perf_counter,
) -> Decorator:
    factor = {"s": 1.0, "ms": 1e3, "us": 1e6}[unit]

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        name = label or func.__name__

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = clock()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed = (clock() - start) * factor
                logger(f"[timed] {name} took {elapsed:.3f} {unit}")

        return wrapper

    return decorator


def retries(
    attempts: int = 3,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
    delay: float = 0.0,
    backoff: float = 1.0,
    jitter: float = 0.0,
    *,
    sleep: Callable[[float], None] = time.sleep,
    logger: Callable[[str], None] = noop_logger,
) -> Decorator:
    assert attempts >= 1

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_error: BaseException | None = None
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as error:
                    last_error = error
                    if attempt == attempts:
                        logger(f"[retries] fail after {attempt} attempts: {error!r}")
                        break
                    wait = delay * (backoff ** (attempt - 1)) + (random.random() * jitter if jitter else 0.0)
                    logger(f"[retries] attempt {attempt} failed: {error!r}; sleeping {wait:.3f}s")
                    sleep(wait)
            assert last_error is not None
            raise last_error

        return wrapper

    return decorator


def make_key(args: tuple[Any, ...], kwargs: dict[str, Any]) -> Hashable:
    return (args, tuple(sorted(kwargs.items())))


def cached(
    *,
    ttl: float | None = None,
    time_fn: Callable[[], float] = time.time,
    logger: Callable[[str], None] = noop_logger,
) -> Decorator:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        cache: dict[Hashable, tuple[float | None, R]] = {}
        stats = {"hits": 0, "misses": 0}
        lock = threading.Lock()

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = make_key(args, kwargs)
            now = time_fn()
            with lock:
                if key in cache:
                    expiry, value = cache[key]
                    if expiry is None or now < expiry:
                        stats["hits"] += 1
                        logger(f"[cached] hit {key}")
                        return value
                    del cache[key]
                stats["misses"] += 1
            logger(f"[cached] miss {key}")
            value = func(*args, **kwargs)
            with lock:
                cache[key] = (None if ttl is None else now + ttl, value)
            return value

        def cache_clear() -> None:
            with lock:
                cache.clear()

        def cache_invalidate(predicate: Callable[[tuple[Any, ...], dict[str, Any]], bool]) -> int:
            removed = 0
            with lock:
                for key in list(cache.keys()):
                    if predicate(key[0], dict(key[1])):
                        del cache[key]
                        removed += 1
            return removed

        def cache_info() -> dict[str, int]:
            with lock:
                return {"hits": stats["hits"], "misses": stats["misses"], "size": len(cache)}

        setattr(wrapper, "cache_clear", cache_clear)
        setattr(wrapper, "cache_invalidate", cache_invalidate)
        setattr(wrapper, "cache_info", cache_info)
        return wrapper

    return decorator


def compose(*decorators: Decorator) -> Decorator:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        return reduce(lambda previous, deco: deco(previous), reversed(decorators), func)

    return decorator

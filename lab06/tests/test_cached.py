from decorators import cached


def test_cached_ttl_and_invalidate():
    t = 1000.0

    def time_fn():
        return t

    hit = {"n": 0}

    @cached(ttl=1.0, time_fn=time_fn)
    def f(x: int) -> int:
        hit["n"] += 1
        return x * 2

    assert f(10) == 20
    assert f(10) == 20
    assert hit["n"] == 1
    t += 2.0
    assert f(10) == 20
    assert hit["n"] == 2
    removed = f.cache_invalidate(lambda a, kw: a == (10,))
    assert removed >= 1
    assert f(10) == 20
    assert hit["n"] == 3


def test_cached_without_ttl_keeps_values():
    calls = {"n": 0}

    @cached(time_fn=lambda: 0.0)
    def square(x: int) -> int:
        calls["n"] += 1
        return x * x

    assert (square(3), square(3), square(4)) == (9, 9, 16)
    assert calls["n"] == 2


def test_cached_key_respects_kwargs():
    calls = {"n": 0}

    @cached(ttl=10.0, time_fn=lambda: 0.0)
    def add(a: int, b: int = 0) -> int:
        calls["n"] += 1
        return a + b

    add(1, b=2)
    add(1, b=3)
    add(1, b=2)
    assert calls["n"] == 2


def test_cache_clear_and_info():
    @cached(ttl=10.0, time_fn=lambda: 0.0)
    def value(x: int) -> int:
        return x

    value(1)
    value(1)
    assert value.cache_info() == {"hits": 1, "misses": 1, "size": 1}
    value.cache_clear()
    assert value.cache_info()["size"] == 0


def test_cached_does_not_store_errors():
    state = {"fail": True}

    @cached(ttl=10.0, time_fn=lambda: 0.0)
    def unreliable() -> str:
        if state["fail"]:
            raise ValueError("fail")
        return "ok"

    try:
        unreliable()
    except ValueError:
        pass
    state["fail"] = False
    assert unreliable() == "ok"


def test_cached_preserves_metadata():
    @cached()
    def documented():
        """Doc."""
        return 1

    assert documented.__name__ == "documented"
    assert documented.__doc__ == "Doc."
    assert documented.__wrapped__ is not None

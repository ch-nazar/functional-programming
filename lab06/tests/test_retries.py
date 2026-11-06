import pytest

from decorators import retries


def test_retries_no_sleep():
    calls = {"n": 0}
    sleeps: list[float] = []

    @retries(attempts=3, delay=0, sleep=sleeps.append, logger=lambda s: None)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("boom")
        return "ok"

    assert flaky() == "ok"
    assert calls["n"] == 3
    assert len(sleeps) == 2


def test_retries_backoff_delays():
    sleeps: list[float] = []

    @retries(attempts=4, delay=0.5, backoff=2.0, sleep=sleeps.append)
    def always_fails():
        raise ConnectionError("down")

    with pytest.raises(ConnectionError):
        always_fails()
    assert sleeps == [0.5, 1.0, 2.0]


def test_retries_raises_last_error_after_attempts():
    calls = {"n": 0}
    logs: list[str] = []

    @retries(attempts=2, sleep=lambda s: None, logger=logs.append)
    def always_fails():
        calls["n"] += 1
        raise ValueError(calls["n"])

    with pytest.raises(ValueError):
        always_fails()
    assert calls["n"] == 2
    assert "fail after 2 attempts" in logs[-1]


def test_retries_ignores_other_exceptions():
    sleeps: list[float] = []

    @retries(attempts=5, exceptions=(ConnectionError,), sleep=sleeps.append)
    def wrong():
        raise KeyError("x")

    with pytest.raises(KeyError):
        wrong()
    assert sleeps == []


def test_retries_jitter_is_added():
    sleeps: list[float] = []
    calls = {"n": 0}

    @retries(attempts=2, delay=1.0, jitter=0.5, sleep=sleeps.append)
    def once_failing():
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("x")
        return 1

    assert once_failing() == 1
    assert 1.0 <= sleeps[0] <= 1.5


def test_retries_preserves_metadata():
    @retries(attempts=2)
    def documented():
        """Doc."""
        return 1

    assert documented.__name__ == "documented"
    assert documented.__doc__ == "Doc."
    assert documented.__wrapped__ is not None

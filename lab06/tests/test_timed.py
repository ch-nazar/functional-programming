import pytest

from decorators import timed


def test_timed_uses_clock_and_logger():
    ticks = [0.0, 0.012345]

    def fake_clock():
        return ticks.pop(0)

    logs: list[str] = []

    @timed("work", unit="ms", logger=logs.append, clock=fake_clock)
    def work(x: int) -> int:
        return x * x

    assert work(5) == 25
    assert any("work took 12.345 ms" in message for message in logs)


def test_timed_uses_function_name_by_default():
    logs: list[str] = []
    ticks = iter([0.0, 2.0])

    @timed(unit="s", logger=logs.append, clock=lambda: next(ticks))
    def slow() -> None:
        return None

    slow()
    assert logs == ["[timed] slow took 2.000 s"]


def test_timed_logs_even_on_error():
    logs: list[str] = []
    ticks = iter([0.0, 1.0])

    @timed("boom", logger=logs.append, clock=lambda: next(ticks))
    def broken() -> None:
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        broken()
    assert len(logs) == 1


def test_timed_preserves_metadata():
    @timed(logger=lambda message: None)
    def documented(x: int) -> int:
        """Doc text."""
        return x

    assert documented.__name__ == "documented"
    assert documented.__doc__ == "Doc text."
    assert documented.__wrapped__ is not None

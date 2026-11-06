from closures import make_controlled_clock, make_counter, make_logger


def test_counter_keeps_independent_state():
    first = make_counter(10)
    second = make_counter()
    assert (first(), first(), second()) == (11, 12, 1)


def test_logger_adds_prefix():
    logs: list[str] = []
    make_logger("INFO", logs.append)("done")
    assert logs == ["[INFO] done"]


def test_controlled_clock():
    clock, advance = make_controlled_clock(5.0)
    advance(2.5)
    assert clock() == 7.5

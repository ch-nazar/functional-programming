from typing import Callable


def make_counter(start: int = 0) -> Callable[[], int]:
    value = start

    def increment() -> int:
        nonlocal value
        value += 1
        return value

    return increment


def make_logger(prefix: str, output: Callable[[str], None] = print) -> Callable[[str], None]:
    def write(message: str) -> None:
        output(f"[{prefix}] {message}")

    return write


def make_controlled_clock(start: float = 0.0) -> tuple[Callable[[], float], Callable[[float], None]]:
    current_time = start

    def clock() -> float:
        return current_time

    def advance(seconds: float) -> None:
        nonlocal current_time
        current_time += seconds

    return clock, advance


def noop_logger(message: str) -> None:
    return None

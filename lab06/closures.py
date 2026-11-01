from typing import Callable


def stvoryty_lichylnyk(pochatok: int = 0) -> Callable[[], int]:
    znachennya = pochatok

    def dodaty_odynytsyu() -> int:
        nonlocal znachennya
        znachennya += 1
        return znachennya

    return dodaty_odynytsyu


def stvoryty_logger(prefiks: str, vyvid: Callable[[str], None] = print) -> Callable[[str], None]:
    def zapysaty(povidomlennya: str) -> None:
        vyvid(f"[{prefiks}] {povidomlennya}")

    return zapysaty


def stvoryty_keruvanyi_hodynnyk(pochatok: float = 0.0) -> tuple[Callable[[], float], Callable[[float], None]]:
    potochnyi_chas = pochatok

    def hodynnyk() -> float:
        return potochnyi_chas

    def peresunuty(sekundy: float) -> None:
        nonlocal potochnyi_chas
        potochnyi_chas += sekundy

    return hodynnyk, peresunuty


def pustyi_zapys(povidomlennya: str) -> None:
    return None

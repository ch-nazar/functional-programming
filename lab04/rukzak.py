from functools import lru_cache
from typing import Callable, Sequence


def perevirity_vkhid(vahy: Sequence[int], tsinnosti: Sequence[int], mistkist: int) -> None:
    if len(vahy) != len(tsinnosti):
        raise ValueError("vahy i tsinnosti maiut buty odnakovoyi dovzhyny")
    if mistkist < 0:
        raise ValueError("mistkist ne mozhe buty vidyemnoyu")
    if any(vaha < 0 for vaha in vahy):
        raise ValueError("vaha ne mozhe buty vidyemnoyu")


def rukzak_bez_keshu(vahy: Sequence[int], tsinnosti: Sequence[int], mistkist: int) -> int:
    perevirity_vkhid(vahy, tsinnosti, mistkist)

    def rozviazaty(indeks: int, zalyshok: int) -> int:
        if indeks == len(vahy):
            return 0
        bez_predmeta = rozviazaty(indeks + 1, zalyshok)
        if vahy[indeks] > zalyshok:
            return bez_predmeta
        z_predmetom = tsinnosti[indeks] + rozviazaty(indeks + 1, zalyshok - vahy[indeks])
        return max(bez_predmeta, z_predmetom)

    return rozviazaty(0, mistkist)


def stvoryty_rozviazuvach(vahy: Sequence[int], tsinnosti: Sequence[int]) -> Callable[[int, int], int]:
    vahy_tuple = tuple(vahy)
    tsinnosti_tuple = tuple(tsinnosti)

    @lru_cache(maxsize=None)
    def rozviazaty(indeks: int, zalyshok: int) -> int:
        if indeks == len(vahy_tuple):
            return 0
        bez_predmeta = rozviazaty(indeks + 1, zalyshok)
        if vahy_tuple[indeks] > zalyshok:
            return bez_predmeta
        z_predmetom = tsinnosti_tuple[indeks] + rozviazaty(indeks + 1, zalyshok - vahy_tuple[indeks])
        return max(bez_predmeta, z_predmetom)

    return rozviazaty


def rukzak_z_keshem(vahy: Sequence[int], tsinnosti: Sequence[int], mistkist: int) -> int:
    perevirity_vkhid(vahy, tsinnosti, mistkist)
    return stvoryty_rozviazuvach(vahy, tsinnosti)(0, mistkist)


def rukzak_iteratyvno(vahy: Sequence[int], tsinnosti: Sequence[int], mistkist: int) -> int:
    perevirity_vkhid(vahy, tsinnosti, mistkist)
    najkrashe = [0] * (mistkist + 1)
    for vaha, tsinnist in zip(vahy, tsinnosti):
        for zalyshok in range(mistkist, vaha - 1, -1):
            najkrashe[zalyshok] = max(najkrashe[zalyshok], najkrashe[zalyshok - vaha] + tsinnist)
    return najkrashe[mistkist]

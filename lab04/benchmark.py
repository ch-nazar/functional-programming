import random
import sys
from timeit import timeit

from rukzak import rukzak_bez_keshu, rukzak_iteratyvno, rukzak_z_keshem, stvoryty_rozviazuvach


def vypadkovi_predmety(kilkist: int):
    random.seed(15)
    vahy = [random.randint(1, 20) for _ in range(kilkist)]
    tsinnosti = [random.randint(1, 100) for _ in range(kilkist)]
    return vahy, tsinnosti


def porivnyaty_chas() -> None:
    for kilkist in (10, 15, 20):
        vahy, tsinnosti = vypadkovi_predmety(kilkist)
        mistkist = 5 * kilkist
        bez = timeit(lambda: rukzak_bez_keshu(vahy, tsinnosti, mistkist), number=1)
        z = timeit(lambda: rukzak_z_keshem(vahy, tsinnosti, mistkist), number=1)
        it = timeit(lambda: rukzak_iteratyvno(vahy, tsinnosti, mistkist), number=1)
        print(f"n={kilkist}: bez keshu {bez:.4f} s, z keshem {z:.4f} s, iteratyvno {it:.4f} s")


def pokazaty_kesh() -> None:
    vahy, tsinnosti = vypadkovi_predmety(20)
    rozviazuvach = stvoryty_rozviazuvach(vahy, tsinnosti)
    print("Rezultat:", rozviazuvach(0, 100))
    print("cache_info:", rozviazuvach.cache_info())
    rozviazuvach.cache_clear()
    print("Pislya cache_clear:", rozviazuvach.cache_info())


def pokazaty_limit_rekursiyi() -> None:
    vahy, tsinnosti = vypadkovi_predmety(5000)
    print("Limit rekursiyi CPython:", sys.getrecursionlimit())
    try:
        rukzak_z_keshem(vahy, tsinnosti, 100)
    except RecursionError:
        print("Rekursivna versiya z n=5000: RecursionError")
    print("Iteratyvna versiya z n=5000:", rukzak_iteratyvno(vahy, tsinnosti, 100))


if __name__ == "__main__":
    porivnyaty_chas()
    pokazaty_kesh()
    pokazaty_limit_rekursiyi()

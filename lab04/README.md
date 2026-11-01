# Lab 4, variant 15: zadacha pro ryukzak 0/1

Bazovyi vypadok: indeks == len(vahy) -> 0. Rekursyvnyi krok: vzyaty abo ne vzyaty predmet.
Versiyi: rukzak_bez_keshu, rukzak_z_keshem (lru_cache na (indeks, zalyshok)), rukzak_iteratyvno.

CPython maye limit rekursiyi (~1000 kadriv, sys.getrecursionlimit()) i ne maye TCO,
tomu rekursiya hlybyny n = kilkist predmetiv padaye z RecursionError, a iteratyvna versiya bezpechna.

Zapusk: python benchmark.py | pytest -q

# Lab 6, variant 15: kompozytsiya dekoratoriv dlya servisnoyi funktsiyi

Zamykannya: stvoryty_lichylnyk (nonlocal), stvoryty_logger, stvoryty_keruvanyi_hodynnyk.
Dekoratory: keshovanyi(ttl), povtory(sproby), vymiryany, ta kompozytsiya skladaty(a, b, c) = a(b(c(f))).
Zalezhnosti (hodynnyk, spy, zapys) peredayutsya yak Callable, tomu testy ne chekayut realnyi sleep.

Poryadok vazhlyvyi:
- kesh -> povtory -> chas: chas vymiryuye kozhnu sprobu, a vluchannya v kesh povnistyu propuskaye povtory ta chas.
- chas -> kesh -> povtory: chas vymiryuye kozhen vyklyk, v tomu chysli vluchannya v kesh.

Zapusk: python main.py | pytest -q

# Лабораторна робота 4. Рекурсія та мемоізація (варіант 15)

**Задача:** рюкзак 0/1 — максимальна цінність предметів за обмеженої місткості.

## Структура
- `algorithms.py` — `knapsack_no_cache`, `knapsack_cached` (`lru_cache` на стані `(index, remaining)`), `knapsack_iterative`, а також `quicksort`, `Node` з обходами, `fib`, `fib_iter`, `fact`.
- `main.py` — демонстрація, `benchmark.py` — порівняння часу та ліміту рекурсії.
- `tests/` — `test_knapsack.py`, `test_quicksort.py`, `test_tree.py`, `test_fib.py`.

## Нотатки
У CPython глибина рекурсії обмежена (приблизно 1000 кадрів, `sys.getrecursionlimit()`), а TCO немає. Тому рекурсивна версія для тисяч предметів падає з `RecursionError`, а ітеративна безпечна.

## Запуск
```
pip install -r requirements.txt
python main.py
python benchmark.py
pytest -q
```

# Лабораторна робота 5. Ліниві обчислення (варіант 15)

**Тема:** потік випадкових вимірювань з інжекцією постачальника значень.

## Структура
- `streams.py` — `measurements`, `valid_only`, `take`, `drop`, `sliding_window`, `moving_average`, `prefix_stats`, `fib_stream`, `naturals`.
- `main.py` — демонстрація; `tests/` — тести з детермінованим постачальником.

## Нотатки
Потік створюється через `iter(callable, sentinel)`. Тести перевіряють лінивість: постачальник викликається лише потрібну кількість разів.

## Запуск
```
pip install -r requirements.txt
python main.py
pytest -q
```

# Лабораторна робота 7. functools та operator (варіант 15)

**Предметна область:** результати лабораторних робіт (студент, лабораторна, бал, спроби, здано).

## Конвеєр
`pipeline` (через `functools.reduce`): нормалізація записів → відбір зданих робіт → створення `LabResult` → підсумковий бал зі штрафом за додаткові спроби (`partial`) → Top-N.

## Використані засоби
- `operator`: `itemgetter`, `attrgetter`, `methodcaller`.
- `functools`: `partial`, `reduce`, `singledispatch`, `total_ordering`.
- `zavantazhyty_zapysy` (singledispatch) приймає рядок (JSON або CSV), `Path` (`.json`/`.csv`), відкритий текстовий файл та список/кортеж записів.
- `LabResult` порівнюється за `(score, attempts, student, lab)`; для чужих типів повертається `NotImplemented`.
- Багатокритеріальне сортування: бал за спаданням, спроби за зростанням, імʼя за зростанням (три стабільні сортування).

## Запуск
```
pip install -r requirements.txt
python main.py
pytest -q
mypy --strict .
black .
ruff check .
```

# Лабораторна робота 7. functools та operator (варіант 15)

**Предметна область:** результати лабораторних робіт (`student`, `lab`, `score`, `attempts`, `submitted`).

## Структура
- `models.py` — `LabResult` з `@total_ordering` за `(score, attempts, student, lab)`.
- `loaders.py` — `load_records` через `singledispatch` для рядка (JSON/CSV), `Path`, файлу та списку.
- `core.py` — `pipeline` (через `reduce`), `normalize_record`, `final_score` (`partial`), `multi_key_sort`, `top_n`, `process`.
- `main.py`, `sample_data.json`, `sample_data.csv`, `tests/test_lab07.py`.

## Запуск
```
pip install -r requirements.txt
python main.py
pytest -q
mypy --strict .
```

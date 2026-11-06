# Лабораторна робота 8. Алгебраїчні типи даних (варіант 15)

**Тема:** абстрактне дерево запитів для фільтрації словників.

## Структура
- `model.py` — вузли `Field`, `Eq`, `And`, `Or`, `Not`, `Query` (`TypeAlias`), `Operator` (`Literal`), `HasName` (`Protocol`).
- `evaluator.py` — `eval_query`, `filter_records`, `query_fields` (через `match/case`, `assert_never`).
- `pretty.py` — `render_query`; `main.py`; `tests/test_query.py`.

Відсутнє поле в записі дає `False`, а не помилку.

## Запуск
```
pip install -r requirements.txt
python main.py
pytest -q
mypy --strict .
```

# Лабораторна робота 8. Алгебраїчні типи даних (варіант 15)

**Тема:** абстрактне дерево запитів для фільтрації словників.

## Модель
- Вузли: `Pole`, `Rivno`, `Ta` (and), `Abo` (or), `Ne` (not) — незмінні `@dataclass(frozen=True)`.
- `Query` — `TypeAlias` обʼєднання вузлів; `Operator` — `Literal`; `MaiePole` — `Protocol`.

## Операції
- `obchyslyty_zapyt` — обчислення запиту для запису (`match/case`).
- `renderyty_zapyt` — текстове представлення запиту.
- `polya_zapytu`, `vidfiltruvaty` — допоміжні операції.
- Усі гілки `match` закриті через `assert_never`. Відсутнє поле в записі дає `False`, а не помилку.

## Запуск
```
pip install -r requirements.txt
python main.py
pytest -q
mypy --strict .
```

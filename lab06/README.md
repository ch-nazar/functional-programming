# Лабораторна робота 6. Замикання та декоратори (варіант 15)

**Тема:** композиція декораторів для сервісної функції.

## Структура
- `closures.py` — `make_counter` (`nonlocal`), `make_logger`, `make_controlled_clock`.
- `decorators.py` — `timed`, `retries`, `cached` (з `cache_clear` і `cache_invalidate`), `compose`.
- `service.py` — нестабільний сервіс для демонстрації; `main.py` — демонстрація порядку декораторів; `tests/`.

## Вплив порядку декораторів
- `cached → retries → timed`: час вимірюється для кожної спроби, а влучання в кеш пропускає повтори й вимірювання.
- `timed → cached → retries`: час вимірюється для кожного виклику, зокрема й для влучання в кеш.

Годинник, `sleep` і логер передаються як `Callable`, тому тести не чекають реального часу.

## Запуск
```
pip install -r requirements.txt
python main.py
pytest -q
```

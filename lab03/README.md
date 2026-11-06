# Лабораторна робота 3. Незмінні структури даних (варіант 15)

**Предметна область:** система задач проєкту.

## Структура
- `model.py` — `Comment`, `Task` (`@dataclass(frozen=True, slots=True)`), `make_metadata`.
- `core.py` — чисті оновлення: `create_task`, `add_comment`, `add_label`, `change_status`, `change_priority`, `update_metadata`, `freeze`.
- `tests/test_immutability.py`, `tests/test_performance.py`, `benchmark.py`, `main.py`.

## Рішення
- Коментарі — `tuple`, мітки — `frozenset`, метадані — `MappingProxyType` над копією словника.
- `Comment` хешується повністю. У `Task` поле `metadata` виключено з хешу (`field(hash=False)`), бо `MappingProxyType` над `dict` не хешується.
- Незмінна версія повільніша через копіювання, але безпечніша.

## Запуск
```
pip install -r requirements.txt
python main.py
python benchmark.py
pytest -q --durations=5
```

# Лабораторна робота 3. Незмінні структури даних (варіант 15)

**Предметна область:** система задач проєкту.

## Модель
- `Komentar` — коментар до задачі (автор, текст).
- `Zadacha` — задача: `id`, `nazva`, `status`, `priorytet`, `komentari` (tuple), `mitky` (frozenset), `metadani` (MappingProxyType).
- Обидві сутності — `@dataclass(frozen=True, slots=True)`.

## Чисті оновлення (повертають нову копію)
`dodaty_komentar`, `dodaty_mitku`, `zminyty_status`, `zminyty_priorytet`, `zminyty_metadani`.

## Хешування
`Komentar` хешується повністю. У `Zadacha` поле `metadani` виключено з хешу (`field(hash=False)`), бо `MappingProxyType` над `dict` не хешується.

## Порівняння часу
`benchmark.py` порівнює змінну версію (list/set/dict) і незмінну (tuple/frozenset). Незмінна версія повільніша через копіювання кортежів, але безпечніша: немає прихованих змін, а об'єкти хешуються.

## Запуск
```
pip install -r requirements.txt
python main.py
python benchmark.py
pytest -q --durations=5
```

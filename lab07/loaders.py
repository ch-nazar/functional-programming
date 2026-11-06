import csv
import io
import json
from functools import singledispatch
from pathlib import Path
from typing import Any

Record = dict[str, Any]


def parse_json(text: str) -> list[Record]:
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError("JSON maye mistyty spysok zapysiv")
    return data


def parse_csv(text: str) -> list[Record]:
    return list(csv.DictReader(io.StringIO(text)))


@singledispatch
def load_records(source: Any) -> list[Record]:
    raise TypeError(f"nepidtrymuvanyi typ dzherela: {type(source).__name__}")


@load_records.register(str)
def _(text: str) -> list[Record]:
    first_char = text.lstrip()[:1]
    return parse_json(text) if first_char in ("[", "{") else parse_csv(text)


@load_records.register(Path)
def _(file_path: Path) -> list[Record]:
    parsers = {".json": parse_json, ".csv": parse_csv}
    if file_path.suffix.lower() not in parsers:
        raise ValueError(f"nevidomyi format fajlu: {file_path.suffix}")
    return parsers[file_path.suffix.lower()](file_path.read_text(encoding="utf-8"))


@load_records.register(io.TextIOBase)
def _(file: io.TextIOBase) -> list[Record]:
    return load_records(file.read())


@load_records.register(list)
@load_records.register(tuple)
def _(collection: list[Record] | tuple[Record, ...]) -> list[Record]:
    return list(collection)

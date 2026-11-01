import csv
import io
import json
from functools import singledispatch
from pathlib import Path
from typing import Any

Zapys = dict[str, Any]


def rozibraty_json(tekst: str) -> list[Zapys]:
    dani = json.loads(tekst)
    if not isinstance(dani, list):
        raise ValueError("JSON maye mistyty spysok zapysiv")
    return dani


def rozibraty_csv(tekst: str) -> list[Zapys]:
    return list(csv.DictReader(io.StringIO(tekst)))


@singledispatch
def zavantazhyty_zapysy(dzherelo: Any) -> list[Zapys]:
    raise TypeError(f"nepidtrymuvanyi typ dzherela: {type(dzherelo).__name__}")


@zavantazhyty_zapysy.register(str)
def _(tekst: str) -> list[Zapys]:
    pochatok = tekst.lstrip()[:1]
    return rozibraty_json(tekst) if pochatok in ("[", "{") else rozibraty_csv(tekst)


@zavantazhyty_zapysy.register(Path)
def _(shlyakh: Path) -> list[Zapys]:
    formaty = {".json": rozibraty_json, ".csv": rozibraty_csv}
    if shlyakh.suffix.lower() not in formaty:
        raise ValueError(f"nevidomyi format fajlu: {shlyakh.suffix}")
    return formaty[shlyakh.suffix.lower()](shlyakh.read_text(encoding="utf-8"))


@zavantazhyty_zapysy.register(io.TextIOBase)
def _(fajl: io.TextIOBase) -> list[Zapys]:
    return zavantazhyty_zapysy(fajl.read())


@zavantazhyty_zapysy.register(list)
@zavantazhyty_zapysy.register(tuple)
def _(kolektsiya: list[Zapys] | tuple[Zapys, ...]) -> list[Zapys]:
    return list(kolektsiya)

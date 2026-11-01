import io
from functools import partial
from pathlib import Path

import pytest

from core import (bahatokryterialne_sortuvannya, normalizuvaty_zapys, obrobyty, pidsumkovyi_bal,
                  pipeline, rozibraty_zdano, top_n, zahalnyi_bal)
from loaders import zavantazhyty_zapysy
from models import LabResult

PAPKA = Path(__file__).parent.parent
ZAPYSY = [
    {"student": " ira ", "lab": "lab1", "score": "90", "attempts": "1", "submitted": "true"},
    {"student": "oleh", "lab": "lab1", "score": "90", "attempts": "3", "submitted": "yes"},
    {"student": "dana", "lab": "lab1", "score": "50", "attempts": "1", "submitted": "false"},
]


def rezultat(student="A", lab="L1", score=50.0, attempts=1, submitted=True):
    return LabResult(student, lab, score, attempts, submitted)


def test_pipeline_zastosovuye_funktsiyi_po_cherzi():
    assert pipeline(3, lambda x: x + 1, lambda x: x * 2) == 8
    assert pipeline(5) == 5


def test_partial_u_konveyeri():
    shtraf = partial(pidsumkovyi_bal, 5.0, 100.0)
    assert shtraf(rezultat(score=90.0, attempts=3)).score == 80.0
    assert partial(top_n, 1)([rezultat("A", score=1.0), rezultat("B", score=2.0)])[0].student == "B"


def test_pidsumkovyi_bal_meji():
    assert pidsumkovyi_bal(2.0, 100.0, rezultat(score=120.0)).score == 100.0
    assert pidsumkovyi_bal(50.0, 100.0, rezultat(score=10.0, attempts=5)).score == 0.0


def test_normalizatsiya_operator_itemgetter_methodcaller():
    zapys = normalizuvaty_zapys(ZAPYSY[0])
    assert zapys == {"student": "Ira", "lab": "LAB1", "score": 90.0, "attempts": 1, "submitted": True}


def test_rozibraty_zdano():
    assert rozibraty_zdano(True) and rozibraty_zdano("Yes") and rozibraty_zdano(" TRUE ")
    assert not rozibraty_zdano(False) and not rozibraty_zdano("no")


def test_zavantazhennya_zi_spysku_ta_kortezha():
    assert zavantazhyty_zapysy(ZAPYSY) == ZAPYSY
    assert zavantazhyty_zapysy(tuple(ZAPYSY)) == ZAPYSY


def test_zavantazhennya_z_json_ryadka_i_csv_ryadka():
    json_ryadok = '[{"student": "a", "lab": "l", "score": 1, "attempts": 1, "submitted": true}]'
    csv_ryadok = "student,lab,score,attempts,submitted\na,l,1,1,true\n"
    assert zavantazhyty_zapysy(json_ryadok)[0]["student"] == "a"
    assert zavantazhyty_zapysy(csv_ryadok)[0]["score"] == "1"


def test_zavantazhennya_z_path_json_ta_csv():
    assert len(zavantazhyty_zapysy(PAPKA / "sample_data.json")) == 5
    assert len(zavantazhyty_zapysy(PAPKA / "sample_data.csv")) == 5


def test_zavantazhennya_z_vidkrytoho_fajlu_ta_stringio():
    with open(PAPKA / "sample_data.json", encoding="utf-8") as fajl:
        assert len(zavantazhyty_zapysy(fajl)) == 5
    assert len(zavantazhyty_zapysy(io.StringIO("student,lab,score,attempts,submitted\na,l,1,1,true\n"))) == 1


def test_zavantazhennya_pomylky():
    with pytest.raises(TypeError):
        zavantazhyty_zapysy(42)
    with pytest.raises(ValueError):
        zavantazhyty_zapysy(PAPKA / "main.py")
    with pytest.raises(ValueError):
        zavantazhyty_zapysy('{"a": 1}')


def test_obrobyty_vidbyraye_zdani_i_robyt_top():
    top = obrobyty(ZAPYSY, 5, shtraf_za_sprobu=2.0)
    assert [r.student for r in top] == ["Ira", "Oleh"]
    assert [r.score for r in top] == [90.0, 86.0]


def test_obrobyty_obmezhuye_n():
    assert len(obrobyty(ZAPYSY, 1)) == 1
    assert obrobyty(ZAPYSY, 0) == []
    assert obrobyty([], 3) == []


def test_bahatokryterialne_sortuvannya():
    vkhid = [rezultat("B", score=80.0, attempts=1), rezultat("A", score=80.0, attempts=1),
             rezultat("C", score=80.0, attempts=2), rezultat("D", score=90.0, attempts=5)]
    vidpovid = bahatokryterialne_sortuvannya(vkhid)
    assert [r.student for r in vidpovid] == ["D", "A", "B", "C"]


def test_zahalnyi_bal_reduce():
    assert zahalnyi_bal([rezultat(score=1.5), rezultat(score=2.5)]) == 4.0
    assert zahalnyi_bal([]) == 0.0


def test_vsi_operatory_porivnyannya():
    menshyi = rezultat("A", score=10.0)
    bilshyi = rezultat("A", score=20.0)
    assert menshyi < bilshyi and menshyi <= bilshyi
    assert bilshyi > menshyi and bilshyi >= menshyi
    assert menshyi != bilshyi and menshyi == rezultat("A", score=10.0)
    assert menshyi <= rezultat("A", score=10.0) and menshyi >= rezultat("A", score=10.0)


def test_porivnyannya_za_sprobamy_potim_za_studentom():
    assert rezultat("Z", score=10.0, attempts=1) < rezultat("A", score=10.0, attempts=2)
    assert rezultat("A", score=10.0) < rezultat("B", score=10.0)


def test_chuzhi_typy_dayut_not_implemented():
    ya = rezultat()
    assert ya.__lt__(5) is NotImplemented
    assert ya.__eq__("abc") is NotImplemented
    assert ya != 5 and not (ya == 5)
    with pytest.raises(TypeError):
        ya < 5


def test_hash_uzghodzhenyi_z_eq():
    assert hash(rezultat("A")) == hash(rezultat("A"))
    assert len({rezultat("A"), rezultat("A"), rezultat("B")}) == 2

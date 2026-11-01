import dataclasses
import pytest

from evaluator import nazva_polya, obchyslyty_zapyt, polya_zapytu, vidfiltruvaty
from model import Abo, Ne, Pole, Rivno, Ta
from pretty import renderyty_zapyt

REKORD = {"status": "open", "priorytet": 1, "terminova": True, "pusto": ""}


def test_pole_perevirya_istynnist():
    assert obchyslyty_zapyt(Pole("terminova"), REKORD)
    assert not obchyslyty_zapyt(Pole("pusto"), REKORD)


def test_rivno():
    assert obchyslyty_zapyt(Rivno(Pole("status"), "open"), REKORD)
    assert not obchyslyty_zapyt(Rivno(Pole("status"), "closed"), REKORD)


def test_ta_abo_ne():
    spravdi = Rivno(Pole("status"), "open")
    hybne = Rivno(Pole("status"), "closed")
    assert obchyslyty_zapyt(Ta(spravdi, spravdi), REKORD)
    assert not obchyslyty_zapyt(Ta(spravdi, hybne), REKORD)
    assert obchyslyty_zapyt(Abo(hybne, spravdi), REKORD)
    assert not obchyslyty_zapyt(Abo(hybne, hybne), REKORD)
    assert obchyslyty_zapyt(Ne(hybne), REKORD)
    assert not obchyslyty_zapyt(Ne(spravdi), REKORD)


def test_vkladenyi_zapyt():
    zapyt = Ta(Rivno(Pole("status"), "open"), Abo(Rivno(Pole("priorytet"), 5), Ne(Rivno(Pole("terminova"), False))))
    assert obchyslyty_zapyt(zapyt, REKORD)
    assert not obchyslyty_zapyt(zapyt, {**REKORD, "terminova": False})


def test_vidsutnie_pole_daye_false():
    assert not obchyslyty_zapyt(Pole("nemaye"), REKORD)
    assert not obchyslyty_zapyt(Rivno(Pole("nemaye"), None), REKORD)
    assert obchyslyty_zapyt(Ne(Rivno(Pole("nemaye"), 1)), REKORD)


def test_porozhnye_imya_polya():
    with pytest.raises(ValueError):
        Pole("")


def test_nezminnist_vuzliv_i_danykh():
    zapyt = Rivno(Pole("status"), "open")
    with pytest.raises(dataclasses.FrozenInstanceError):
        zapyt.znachennya = "closed"
    kopiya = dict(REKORD)
    obchyslyty_zapyt(Ne(zapyt), kopiya)
    assert kopiya == REKORD


def test_vuzly_hashovani_i_rivni():
    assert Rivno(Pole("a"), 1) == Rivno(Pole("a"), 1)
    assert len({Pole("a"), Pole("a"), Pole("b")}) == 2


def test_vidfiltruvaty_ne_zminyuye_spysok():
    rekordy = [{"x": 1}, {"x": 2}, {"x": 1}]
    rezultat = vidfiltruvaty(Rivno(Pole("x"), 1), rekordy)
    assert rezultat == [{"x": 1}, {"x": 1}]
    assert len(rekordy) == 3
    assert vidfiltruvaty(Rivno(Pole("x"), 1), []) == []


def test_render():
    zapyt = Ta(Rivno(Pole("status"), "open"), Abo(Pole("terminova"), Ne(Rivno(Pole("priorytet"), 3))))
    assert renderyty_zapyt(zapyt) == "(status == 'open' and (terminova or not priorytet == 3))"
    assert renderyty_zapyt(Rivno(Pole("a"), None)) == "a == None"


def test_polya_zapytu_i_protocol():
    zapyt = Ta(Rivno(Pole("a"), 1), Ne(Abo(Pole("b"), Pole("a"))))
    assert polya_zapytu(zapyt) == frozenset({"a", "b"})
    assert nazva_polya(Pole("x")) == "x"


def test_nevidomyi_vuzol():
    with pytest.raises(AssertionError):
        obchyslyty_zapyt("ne zapyt", REKORD)
    with pytest.raises(AssertionError):
        renderyty_zapyt(42)

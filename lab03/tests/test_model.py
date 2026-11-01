import dataclasses
import pytest

from model import (Komentar, Zadacha, dodaty_komentar, dodaty_mitku, stvoryty_zadachu,
                   zminyty_metadani, zminyty_priorytet, zminyty_status, zrobyty_metadani)


def test_dodaty_komentar_ne_zminyuye_staru_zadachu():
    persha = stvoryty_zadachu(1, "a")
    druha = dodaty_komentar(persha, Komentar("Ira", "ok"))
    assert persha.komentari == ()
    assert druha.komentari == (Komentar("Ira", "ok"),)
    assert persha is not druha


def test_dodaty_mitku_ne_zminyuye_staru_zadachu():
    persha = stvoryty_zadachu(1, "a")
    druha = dodaty_mitku(persha, "bug")
    assert persha.mitky == frozenset()
    assert druha.mitky == frozenset({"bug"})


def test_zminyty_status_i_priorytet():
    persha = stvoryty_zadachu(1, "a")
    druha = zminyty_priorytet(zminyty_status(persha, "zrobleno"), 5)
    assert (persha.status, persha.priorytet) == ("todo", 3)
    assert (druha.status, druha.priorytet) == ("zrobleno", 5)


def test_pohanyi_priorytet():
    with pytest.raises(ValueError):
        zminyty_priorytet(stvoryty_zadachu(1, "a"), 9)


def test_pryamu_zminu_polya_zaboroneno():
    zadacha = stvoryty_zadachu(1, "a")
    with pytest.raises(dataclasses.FrozenInstanceError):
        zadacha.status = "zrobleno"


def test_metadani_tilky_dlya_chytannya():
    zadacha = stvoryty_zadachu(1, "a", avtor="Ira")
    with pytest.raises(TypeError):
        zadacha.metadani["avtor"] = "Oleh"


def test_metadani_kopiyuyutsya_z_dzherela():
    dzherelo = {"klyuch": "1"}
    metadani = zrobyty_metadani(**dzherelo)
    dzherelo["klyuch"] = "2"
    assert metadani["klyuch"] == "1"


def test_zminyty_metadani_daye_novu_zadachu():
    persha = stvoryty_zadachu(1, "a", avtor="Ira")
    druha = zminyty_metadani(persha, avtor="Oleh", sprint="3")
    assert persha.metadani["avtor"] == "Ira"
    assert dict(druha.metadani) == {"avtor": "Oleh", "sprint": "3"}


def test_zadacha_i_komentar_hashovani():
    zadacha = dodaty_komentar(stvoryty_zadachu(1, "a", x="y"), Komentar("Ira", "ok"))
    assert isinstance(hash(zadacha), int)
    assert len({zadacha, zadacha}) == 1
    assert hash(Komentar("Ira", "ok")) == hash(Komentar("Ira", "ok"))


def test_zadachi_z_odnakovymy_polyamy_rivni():
    assert stvoryty_zadachu(1, "a") == stvoryty_zadachu(1, "a")


def test_typy_kolektsiy():
    zadacha = stvoryty_zadachu(1, "a")
    assert isinstance(zadacha, Zadacha)
    assert isinstance(zadacha.komentari, tuple)
    assert isinstance(zadacha.mitky, frozenset)

import pytest

from potik import (dopustymi, kovzne_vikno, prefiksni_statystyky, propustyty,
                   ruhome_serednye, vymiryuvannya, vzyaty)


def stvoryty_postachalnyka(znachennya):
    dzherelo = iter(znachennya)
    vyklyky = {"kilkist": 0}

    def postachalnyk():
        vyklyky["kilkist"] += 1
        return next(dzherelo, None)

    return postachalnyk, vyklyky


def test_vymiryuvannya_zupynyayetsya_na_storozhi():
    postachalnyk, _ = stvoryty_postachalnyka([1.0, 2.0, 3.0])
    assert list(vymiryuvannya(postachalnyk)) == [1.0, 2.0, 3.0]


def test_porozhnye_dzherelo():
    postachalnyk, _ = stvoryty_postachalnyka([])
    assert list(vymiryuvannya(postachalnyk)) == []
    assert vzyaty(3, iter([])) == []


def test_dopustymi_vidkydaye_nedopustymi():
    assert list(dopustymi([5, -1, 20, 100, 0], 0, 50)) == [5, 20, 0]


def test_vzyaty_nul_i_bilshe_nizh_ye():
    assert vzyaty(0, iter([1, 2, 3])) == []
    assert vzyaty(10, iter([1, 2, 3])) == [1, 2, 3]


def test_propustyty():
    assert list(propustyty(2, iter([1, 2, 3, 4]))) == [3, 4]
    assert list(propustyty(0, iter([1, 2]))) == [1, 2]
    assert list(propustyty(5, iter([1, 2]))) == []


def test_kovzne_vikno():
    assert list(kovzne_vikno([1, 2, 3, 4], 2)) == [(1, 2), (2, 3), (3, 4)]
    assert list(kovzne_vikno([1, 2, 3], 3)) == [(1, 2, 3)]


def test_vikno_bilshe_za_dovzhynu():
    assert list(kovzne_vikno([1, 2], 5)) == []


def test_pohanyi_rozmir_vikna():
    with pytest.raises(ValueError):
        kovzne_vikno([1, 2, 3], 0)
    with pytest.raises(ValueError):
        ruhome_serednye([1, 2, 3], -2)


def test_ruhome_serednye():
    assert list(ruhome_serednye([1, 2, 3, 4], 2)) == [1.5, 2.5, 3.5]


def test_prefiksni_statystyky():
    rezultat = list(prefiksni_statystyky([4, 2, 6]))
    assert rezultat == [(1, 4, 4, 4, 4.0), (2, 6, 2, 4, 3.0), (3, 12, 2, 6, 4.0)]


def test_lenivist_postachalnyka():
    postachalnyk, vyklyky = stvoryty_postachalnyka([5, 100, 7, 8, 9, 10])
    potik = dopustymi(vymiryuvannya(postachalnyk), 0, 50)
    assert vzyaty(2, potik) == [5, 7]
    assert vyklyky["kilkist"] == 3


def test_lenivist_ruhomoho_serednoho():
    postachalnyk, vyklyky = stvoryty_postachalnyka(range(1, 100))
    potik = ruhome_serednye(vymiryuvannya(postachalnyk), 3)
    assert vzyaty(2, potik) == [2.0, 3.0]
    assert vyklyky["kilkist"] == 4


def test_lenivist_prefiksnykh_statystyk():
    postachalnyk, vyklyky = stvoryty_postachalnyka(range(1, 100))
    vzyaty(3, prefiksni_statystyky(vymiryuvannya(postachalnyk)))
    assert vyklyky["kilkist"] == 3


def test_neskinchenyi_potik_ne_zavisaye():
    postachalnyk = lambda: 1.0
    assert vzyaty(3, ruhome_serednye(vymiryuvannya(postachalnyk), 2)) == [1.0, 1.0, 1.0]

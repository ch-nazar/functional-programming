import pytest

from closures import stvoryty_keruvanyi_hodynnyk, stvoryty_lichylnyk, stvoryty_logger
from decorators import keshovanyi, povtory, skladaty, vymiryany
from servis import stvoryty_nestabilnyi_servis


def test_lichylnyk_trymaye_stan_nezalezhno():
    persha = stvoryty_lichylnyk(10)
    druha = stvoryty_lichylnyk()
    assert (persha(), persha(), druha()) == (11, 12, 1)


def test_logger_dodaye_prefiks():
    zapysy: list[str] = []
    stvoryty_logger("INFO", zapysy.append)("hotovo")
    assert zapysy == ["[INFO] hotovo"]


def test_keruvanyi_hodynnyk():
    hodynnyk, peresunuty = stvoryty_keruvanyi_hodynnyk(5.0)
    peresunuty(2.5)
    assert hodynnyk() == 7.5


def test_metadani_zberihayutsya_u_vsikh_dekoratoriv():
    servis, _ = stvoryty_nestabilnyi_servis(0)
    for dekorator in (vymiryany(), povtory(2), keshovanyi(1.0), skladaty(keshovanyi(1.0), povtory(2), vymiryany())):
        obgornutyi = dekorator(servis)
        assert obgornutyi.__name__ == "otrymaty_profil"
        assert obgornutyi.__doc__ == "Povertaye profil korystuvacha."
        assert obgornutyi.__wrapped__ is not None


def test_vymiryany_zapysuye_chas():
    hodynnyk, peresunuty = stvoryty_keruvanyi_hodynnyk()
    zapysy: list[str] = []

    @vymiryany(hodynnyk, zapysy.append)
    def povilna() -> int:
        peresunuty(2.0)
        return 5

    assert povilna() == 5
    assert zapysy == ["povilna trvala 2.000 s"]


def test_vymiryany_zapysuye_chas_navit_pry_pomyltsi():
    hodynnyk, peresunuty = stvoryty_keruvanyi_hodynnyk()
    zapysy: list[str] = []

    @vymiryany(hodynnyk, zapysy.append)
    def zlamana() -> None:
        peresunuty(1.0)
        raise RuntimeError("bum")

    with pytest.raises(RuntimeError):
        zlamana()
    assert len(zapysy) == 1


def test_povtory_uspikh_pislya_zbiyiv_bez_realnoho_sleep():
    paused: list[float] = []
    servis, skilky = stvoryty_nestabilnyi_servis(2)
    obgornutyi = povtory(3, (ConnectionError,), 0.5, paused.append)(servis)
    assert obgornutyi(1) == "profil_1"
    assert skilky() == 3
    assert paused == [0.5, 0.5]


def test_povtory_vyclerpuye_sproby():
    paused: list[float] = []
    servis, skilky = stvoryty_nestabilnyi_servis(10)
    obgornutyi = povtory(3, (ConnectionError,), 0.1, paused.append)(servis)
    with pytest.raises(ConnectionError):
        obgornutyi(1)
    assert skilky() == 3
    assert len(paused) == 2


def test_povtory_ne_lovyt_chuzhi_vynyatky():
    paused: list[float] = []

    @povtory(5, (ConnectionError,), 0.1, paused.append)
    def pohana() -> None:
        raise KeyError("x")

    with pytest.raises(KeyError):
        pohana()
    assert paused == []


def test_povtory_pohani_sproby():
    with pytest.raises(ValueError):
        povtory(0)


def test_kesh_vluchannya_i_promakhy():
    hodynnyk, _ = stvoryty_keruvanyi_hodynnyk()
    vykyky: list[int] = []

    @keshovanyi(10.0, hodynnyk)
    def kvadrat(x: int) -> int:
        vykyky.append(x)
        return x * x

    assert kvadrat(3) == 9 and kvadrat(3) == 9 and kvadrat(4) == 16
    assert vykyky == [3, 4]
    assert kvadrat.cache_info() == {"vluchannya": 1, "promakhy": 2, "rozmir": 2}


def test_kesh_ttl_zakinchuyetsya():
    hodynnyk, peresunuty = stvoryty_keruvanyi_hodynnyk()
    vykyky: list[int] = []

    @keshovanyi(5.0, hodynnyk)
    def tochka(x: int) -> int:
        vykyky.append(x)
        return x

    tochka(1)
    peresunuty(4.9)
    tochka(1)
    peresunuty(0.2)
    tochka(1)
    assert vykyky == [1, 1]


def test_kesh_vrakhovuye_kwargs_i_cache_clear():
    hodynnyk, _ = stvoryty_keruvanyi_hodynnyk()
    vykyky: list[int] = []

    @keshovanyi(10.0, hodynnyk)
    def dodaty(a: int, b: int = 0) -> int:
        vykyky.append(1)
        return a + b

    dodaty(1, b=2)
    dodaty(1, b=3)
    dodaty(1, b=2)
    assert len(vykyky) == 2
    dodaty.cache_clear()
    assert dodaty.cache_info()["rozmir"] == 0
    dodaty(1, b=2)
    assert len(vykyky) == 3


def test_kesh_ne_zberigaye_pomylky():
    hodynnyk, _ = stvoryty_keruvanyi_hodynnyk()
    stan = {"pomylka": True}

    @keshovanyi(10.0, hodynnyk)
    def nenadiina() -> str:
        if stan["pomylka"]:
            raise ValueError("zbiy")
        return "ok"

    with pytest.raises(ValueError):
        nenadiina()
    stan["pomylka"] = False
    assert nenadiina() == "ok"


def test_poryadok_dekoratoriv_zminyuye_kilkist_vymiriv():
    rezultaty = {}
    for nazva in ("kesh_zovni", "chas_zovni"):
        hodynnyk, peresunuty = stvoryty_keruvanyi_hodynnyk()
        chasovi: list[str] = []
        servis, skilky = stvoryty_nestabilnyi_servis(2)
        kesh = keshovanyi(60.0, hodynnyk)
        povtor = povtory(3, (ConnectionError,), 0.0, peresunuty)
        chas = vymiryany(hodynnyk, chasovi.append)
        poryadok = (kesh, povtor, chas) if nazva == "kesh_zovni" else (chas, kesh, povtor)
        obgornutyi = skladaty(*poryadok)(servis)
        obgornutyi(1)
        obgornutyi(1)
        rezultaty[nazva] = (len(chasovi), skilky())
    assert rezultaty["kesh_zovni"] == (3, 3)
    assert rezultaty["chas_zovni"] == (2, 3)


def test_poryadok_dekoratoriv_zminyuye_vluchannya_keshu():
    hodynnyk, _ = stvoryty_keruvanyi_hodynnyk()
    servis, _ = stvoryty_nestabilnyi_servis(2)
    kesh = keshovanyi(60.0, hodynnyk)
    obgornutyi = skladaty(povtory(3, (ConnectionError,), 0.0, lambda s: None), kesh)(servis)
    obgornutyi(1)
    obgornutyi(1)
    info = obgornutyi.__wrapped__.cache_info()
    assert info["promakhy"] == 3
    assert info["vluchannya"] == 1

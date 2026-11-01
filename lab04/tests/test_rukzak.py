import random
import pytest

from rukzak import rukzak_bez_keshu, rukzak_iteratyvno, rukzak_z_keshem, stvoryty_rozviazuvach

VAHY = (1, 3, 4, 5)
TSINNOSTI = (1, 4, 5, 7)


def test_klasychnyi_pryklad():
    assert rukzak_bez_keshu(VAHY, TSINNOSTI, 7) == 9
    assert rukzak_z_keshem(VAHY, TSINNOSTI, 7) == 9
    assert rukzak_iteratyvno(VAHY, TSINNOSTI, 7) == 9


def test_nulova_mistkist():
    assert rukzak_bez_keshu(VAHY, TSINNOSTI, 0) == 0
    assert rukzak_z_keshem(VAHY, TSINNOSTI, 0) == 0
    assert rukzak_iteratyvno(VAHY, TSINNOSTI, 0) == 0


def test_porozhni_predmety():
    assert rukzak_bez_keshu([], [], 10) == 0
    assert rukzak_z_keshem([], [], 10) == 0
    assert rukzak_iteratyvno([], [], 10) == 0


def test_zhoden_predmet_ne_vlazyt():
    assert rukzak_z_keshem([10, 20], [5, 6], 9) == 0


def test_vsi_predmety_vlazyat():
    assert rukzak_z_keshem([1, 2, 3], [10, 20, 30], 100) == 60


def test_predmet_rivno_po_mistkosti():
    assert rukzak_z_keshem([5], [8], 5) == 8


def test_vkhid_ne_zminyuyetsya():
    vahy = [1, 3, 4, 5]
    tsinnosti = [1, 4, 5, 7]
    rukzak_z_keshem(vahy, tsinnosti, 7)
    assert vahy == [1, 3, 4, 5] and tsinnosti == [1, 4, 5, 7]


def test_trii_versiyi_zbihayutsya_na_vypadkovykh_danykh():
    random.seed(1)
    for _ in range(30):
        n = random.randint(0, 10)
        vahy = [random.randint(0, 8) for _ in range(n)]
        tsinnosti = [random.randint(0, 50) for _ in range(n)]
        mistkist = random.randint(0, 25)
        ochikuvane = rukzak_iteratyvno(vahy, tsinnosti, mistkist)
        assert rukzak_bez_keshu(vahy, tsinnosti, mistkist) == ochikuvane
        assert rukzak_z_keshem(vahy, tsinnosti, mistkist) == ochikuvane


def test_pohani_dani():
    with pytest.raises(ValueError):
        rukzak_z_keshem([1, 2], [1], 5)
    with pytest.raises(ValueError):
        rukzak_z_keshem([1], [1], -1)
    with pytest.raises(ValueError):
        rukzak_iteratyvno([-1], [1], 5)


def test_kesh_pratsyuye_i_ochyshchuyetsya():
    rozviazuvach = stvoryty_rozviazuvach([1] * 6, [1] * 6)
    assert rozviazuvach(0, 4) == 4
    assert rozviazuvach.cache_info().currsize > 0
    assert rozviazuvach.cache_info().hits > 0
    rozviazuvach.cache_clear()
    assert rozviazuvach.cache_info().currsize == 0


def test_kesh_robyt_menshe_vykliv_nizh_stany_bez_keshu():
    rozviazuvach = stvoryty_rozviazuvach([1] * 20, [1] * 20)
    rozviazuvach(0, 10)
    assert rozviazuvach.cache_info().currsize <= 20 * 11


def test_gluboka_rekursiya_padaye_a_iteratyvna_ni():
    vahy = [1] * 3000
    tsinnosti = [2] * 3000
    with pytest.raises(RecursionError):
        rukzak_z_keshem(vahy, tsinnosti, 10)
    assert rukzak_iteratyvno(vahy, tsinnosti, 10) == 20

from closures import stvoryty_keruvanyi_hodynnyk, stvoryty_logger
from decorators import keshovanyi, povtory, skladaty, vymiryany
from servis import stvoryty_nestabilnyi_servis


def pokazaty_poryadok(nazva: str, poryadok_za_nazvoyu: str) -> None:
    print(f"\n=== {nazva} ===")
    hodynnyk, peresunuty = stvoryty_keruvanyi_hodynnyk()
    zapys = stvoryty_logger("log")
    servis, _ = stvoryty_nestabilnyi_servis(kilkist_zbiyiv=2)

    def povilnyi_spy(sekundy: float) -> None:
        peresunuty(sekundy)

    kesh = keshovanyi(ttl=60, hodynnyk=hodynnyk, zapys=zapys)
    povtor = povtory(sproby=3, zatrymka=0.5, spy=povilnyi_spy, zapys=zapys)
    chas = vymiryany(hodynnyk=hodynnyk, zapys=zapys)
    poryadky = {"kesh_povtor_chas": (kesh, povtor, chas), "chas_kesh_povtor": (chas, kesh, povtor)}
    obgornutyi = skladaty(*poryadky[poryadok_za_nazvoyu])(servis)
    print("Pershyi vyklyk:", obgornutyi(7))
    print("Drugyi vyklyk:", obgornutyi(7))


if __name__ == "__main__":
    pokazaty_poryadok("Poryadok: kesh -> povtory -> chas (chas vymiryuye kozhnu sprobu)", "kesh_povtor_chas")
    pokazaty_poryadok("Poryadok: chas -> kesh -> povtory (chas vymiryuye kozhen vyklyk, v tomu chysli z keshu)", "chas_kesh_povtor")

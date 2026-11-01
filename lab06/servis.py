from typing import Callable


def stvoryty_nestabilnyi_servis(kilkist_zbiyiv: int) -> tuple[Callable[[int], str], Callable[[], int]]:
    sprob = 0

    def otrymaty_profil(id_korystuvacha: int) -> str:
        """Povertaye profil korystuvacha."""
        nonlocal sprob
        sprob += 1
        if sprob <= kilkist_zbiyiv:
            raise ConnectionError(f"zbiy servisu pry sprobi {sprob}")
        return f"profil_{id_korystuvacha}"

    def skilky_vykliv() -> int:
        return sprob

    return otrymaty_profil, skilky_vykliv

from model import Komentar, dodaty_komentar, dodaty_mitku, stvoryty_zadachu, zminyty_priorytet, zminyty_status


def pokazaty(nazva: str, zadacha) -> None:
    print(f"{nazva}: status={zadacha.status}, priorytet={zadacha.priorytet}, "
          f"komentari={zadacha.kilkist_komentariv()}, mitky={sorted(zadacha.mitky)}")


if __name__ == "__main__":
    persha = stvoryty_zadachu(1, "Zrobyty lab 3", proekt="FP")
    pokazaty("Persha", persha)
    druha = dodaty_komentar(persha, Komentar("Ira", "Pochynayu"))
    tretya = dodaty_mitku(druha, "terminovo")
    chetverta = zminyty_priorytet(zminyty_status(tretya, "u_roboti"), 1)
    pokazaty("Persha (ne zminylas)", persha)
    pokazaty("Chetverta (nova kopiya)", chetverta)
    print("Hash chetvertoyi:", hash(chetverta) != 0)

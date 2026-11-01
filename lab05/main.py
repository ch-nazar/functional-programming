from random import Random

from potik import (dopustymi, propustyty, prefiksni_statystyky, ruhome_serednye,
                   vymiryuvannya, vzyaty)


def stvoryty_postachalnyka(zerno: int):
    generator = Random(zerno)
    return lambda: round(generator.uniform(-10, 60), 1)


if __name__ == "__main__":
    postachalnyk = stvoryty_postachalnyka(15)
    dopustymi_znachennya = dopustymi(vymiryuvannya(postachalnyk), 0, 50)
    print("Persha 8 dopustymykh vymiryuvan:", vzyaty(8, dopustymi_znachennya))

    postachalnyk = stvoryty_postachalnyka(15)
    dopustymi_znachennya = dopustymi(vymiryuvannya(postachalnyk), 0, 50)
    print("Ruhome serednye (vikno 3):", [round(x, 2) for x in vzyaty(5, ruhome_serednye(dopustymi_znachennya, 3))])

    postachalnyk = stvoryty_postachalnyka(15)
    dopustymi_znachennya = dopustymi(vymiryuvannya(postachalnyk), 0, 50)
    print("Prefiksni statystyky (kilkist, suma, min, max, serednye):")
    for riadok in vzyaty(4, propustyty(2, prefiksni_statystyky(dopustymi_znachennya))):
        print(riadok)

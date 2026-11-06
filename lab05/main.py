from random import Random

from streams import (valid_only, drop, prefix_stats, moving_average,
                   measurements, take)


def make_provider(seed: int):
    generator = Random(seed)
    return lambda: round(generator.uniform(-10, 60), 1)


if __name__ == "__main__":
    provider = make_provider(15)
    valid_values = valid_only(measurements(provider), 0, 50)
    print("Persha 8 dopustymykh vymiryuvan:", take(8, valid_values))

    provider = make_provider(15)
    valid_values = valid_only(measurements(provider), 0, 50)
    print("Ruhome serednye (vikno 3):", [round(x, 2) for x in take(5, moving_average(valid_values, 3))])

    provider = make_provider(15)
    valid_values = valid_only(measurements(provider), 0, 50)
    print("Prefiksni statystyky (kilkist, suma, min, max, serednye):")
    for row in take(4, drop(2, prefix_stats(valid_values))):
        print(row)

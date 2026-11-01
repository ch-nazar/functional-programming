# Lab 3, variant 15: Zadachi proektu (immutability)

Model: Zadacha, Komentar, mitky (frozenset), metadani (MappingProxyType).
Pure updates: dodaty_komentar, dodaty_mitku, zminyty_status, zminyty_priorytet, zminyty_metadani.

Hashuvannya: Komentar hashovanyi povnistyu. U Zadacha pole metadani vyklyucheno z hash
(field(hash=False)), bo MappingProxyType nad dict ne hashuyetsya.

Zapusk: python main.py | python benchmark.py | pytest -q --durations=5

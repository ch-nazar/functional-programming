# Lab 7, variant 15: rezultaty laboratornykh robit

Konveyer (pipeline cherez functools.reduce):
normalizuvaty -> vidibraty zdani -> LabResult -> pidsumkovyi bal (partial: shtraf za sprobu) -> Top-N.
operator: itemgetter, attrgetter, methodcaller. singledispatch: zavantazhyty_zapysy dlya str (JSON/CSV tekst),
Path (.json/.csv), vidkrytoho tekstovoho fajlu ta spysku/kortezha.
LabResult z @total_ordering porivnyuyetsya za (score, attempts, student, lab); chuzhi typy -> NotImplemented.
Top-N: bal za spadannyam, sprob za zrostannyam, imya za zrostannyam (tri stabilni sortuvannya).

Zapusk: python main.py | pytest -q | mypy --strict . | black . | ruff check .

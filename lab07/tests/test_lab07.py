import io
from functools import partial
from pathlib import Path

import pytest

from core import (multi_key_sort, normalize_record, process, final_score,
                  pipeline, parse_submitted, top_n, total_score)
from loaders import load_records
from models import LabResult

BASE_DIR = Path(__file__).parent.parent
RECORDS = [
    {"student": " ira ", "lab": "lab1", "score": "90", "attempts": "1", "submitted": "true"},
    {"student": "oleh", "lab": "lab1", "score": "90", "attempts": "3", "submitted": "yes"},
    {"student": "dana", "lab": "lab1", "score": "50", "attempts": "1", "submitted": "false"},
]


def result(student="A", lab="L1", score=50.0, attempts=1, submitted=True):
    return LabResult(student, lab, score, attempts, submitted)


def test_pipeline_applies_functions_at_order():
    assert pipeline(3, lambda x: x + 1, lambda x: x * 2) == 8
    assert pipeline(5) == 5


def test_partial_in_pipeline():
    penalty = partial(final_score, 5.0, 100.0)
    assert penalty(result(score=90.0, attempts=3)).score == 80.0
    assert partial(top_n, 1)([result("A", score=1.0), result("B", score=2.0)])[0].student == "B"


def test_final_score_bounds():
    assert final_score(2.0, 100.0, result(score=120.0)).score == 100.0
    assert final_score(50.0, 100.0, result(score=10.0, attempts=5)).score == 0.0


def test_normalization_operator_itemgetter_methodcaller():
    record = normalize_record(RECORDS[0])
    assert record == {"student": "Ira", "lab": "LAB1", "score": 90.0, "attempts": 1, "submitted": True}


def test_parse_submitted():
    assert parse_submitted(True) and parse_submitted("Yes") and parse_submitted(" TRUE ")
    assert not parse_submitted(False) and not parse_submitted("no")


def test_loading_from_list_and_tuple():
    assert load_records(RECORDS) == RECORDS
    assert load_records(tuple(RECORDS)) == RECORDS


def test_loading_from_json_string_and_csv_string():
    json_text = '[{"student": "a", "lab": "l", "score": 1, "attempts": 1, "submitted": true}]'
    csv_text = "student,lab,score,attempts,submitted\na,l,1,1,true\n"
    assert load_records(json_text)[0]["student"] == "a"
    assert load_records(csv_text)[0]["score"] == "1"


def test_loading_from_path_json_and_csv():
    assert len(load_records(BASE_DIR / "sample_data.json")) == 5
    assert len(load_records(BASE_DIR / "sample_data.csv")) == 5


def test_loading_from_open_file_and_stringio():
    with open(BASE_DIR / "sample_data.json", encoding="utf-8") as file:
        assert len(load_records(file)) == 5
    assert len(load_records(io.StringIO("student,lab,score,attempts,submitted\na,l,1,1,true\n"))) == 1


def test_loading_errors():
    with pytest.raises(TypeError):
        load_records(42)
    with pytest.raises(ValueError):
        load_records(BASE_DIR / "main.py")
    with pytest.raises(ValueError):
        load_records('{"a": 1}')


def test_process_selects_submitted_and_makes_top():
    top = process(RECORDS, 5, attempt_penalty=2.0)
    assert [r.student for r in top] == ["Ira", "Oleh"]
    assert [r.score for r in top] == [90.0, 86.0]


def test_process_limits_n():
    assert len(process(RECORDS, 1)) == 1
    assert process(RECORDS, 0) == []
    assert process([], 3) == []


def test_multi_key_sort():
    input_results = [result("B", score=80.0, attempts=1), result("A", score=80.0, attempts=1),
             result("C", score=80.0, attempts=2), result("D", score=90.0, attempts=5)]
    sorted_results = multi_key_sort(input_results)
    assert [r.student for r in sorted_results] == ["D", "A", "B", "C"]


def test_total_score_reduce():
    assert total_score([result(score=1.5), result(score=2.5)]) == 4.0
    assert total_score([]) == 0.0


def test_all_operators_comparison():
    lower = result("A", score=10.0)
    higher = result("A", score=20.0)
    assert lower < higher and lower <= higher
    assert higher > lower and higher >= lower
    assert lower != higher and lower == result("A", score=10.0)
    assert lower <= result("A", score=10.0) and lower >= result("A", score=10.0)


def test_comparison_by_attempts_then_by_student():
    assert result("Z", score=10.0, attempts=1) < result("A", score=10.0, attempts=2)
    assert result("A", score=10.0) < result("B", score=10.0)


def test_foreign_types_give_not_implemented():
    me = result()
    assert me.__lt__(5) is NotImplemented
    assert me.__eq__("abc") is NotImplemented
    assert me != 5 and not (me == 5)
    with pytest.raises(TypeError):
        me < 5


def test_hash_consistent_from_eq():
    assert hash(result("A")) == hash(result("A"))
    assert len({result("A"), result("A"), result("B")}) == 2

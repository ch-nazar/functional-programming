import dataclasses
import pytest

from evaluator import field_name, eval_query, query_fields, filter_records
from model import Or, Not, Field, Eq, And
from pretty import render_query

RECORD = {"status": "open", "priorytet": 1, "terminova": True, "pusto": ""}


def test_field_checks_truthiness():
    assert eval_query(Field("terminova"), RECORD)
    assert not eval_query(Field("pusto"), RECORD)


def test_eq():
    assert eval_query(Eq(Field("status"), "open"), RECORD)
    assert not eval_query(Eq(Field("status"), "closed"), RECORD)


def test_and_or_not():
    true_query = Eq(Field("status"), "open")
    false_query = Eq(Field("status"), "closed")
    assert eval_query(And(true_query, true_query), RECORD)
    assert not eval_query(And(true_query, false_query), RECORD)
    assert eval_query(Or(false_query, true_query), RECORD)
    assert not eval_query(Or(false_query, false_query), RECORD)
    assert eval_query(Not(false_query), RECORD)
    assert not eval_query(Not(true_query), RECORD)


def test_nested_query():
    query = And(Eq(Field("status"), "open"), Or(Eq(Field("priorytet"), 5), Not(Eq(Field("terminova"), False))))
    assert eval_query(query, RECORD)
    assert not eval_query(query, {**RECORD, "terminova": False})


def test_missing_field_gives_false():
    assert not eval_query(Field("nemaye"), RECORD)
    assert not eval_query(Eq(Field("nemaye"), None), RECORD)
    assert eval_query(Not(Eq(Field("nemaye"), 1)), RECORD)


def test_empty_name_field():
    with pytest.raises(ValueError):
        Field("")


def test_immutability_nodes_and_data():
    query = Eq(Field("status"), "open")
    with pytest.raises(dataclasses.FrozenInstanceError):
        query.value = "closed"
    copy_ = dict(RECORD)
    eval_query(Not(query), copy_)
    assert copy_ == RECORD


def test_nodes_hashable_and_equal():
    assert Eq(Field("a"), 1) == Eq(Field("a"), 1)
    assert len({Field("a"), Field("a"), Field("b")}) == 2


def test_filter_not_changes_list():
    records = [{"x": 1}, {"x": 2}, {"x": 1}]
    result = filter_records(Eq(Field("x"), 1), records)
    assert result == [{"x": 1}, {"x": 1}]
    assert len(records) == 3
    assert filter_records(Eq(Field("x"), 1), []) == []


def test_render():
    query = And(Eq(Field("status"), "open"), Or(Field("terminova"), Not(Eq(Field("priorytet"), 3))))
    assert render_query(query) == "(status == 'open' and (terminova or not priorytet == 3))"
    assert render_query(Eq(Field("a"), None)) == "a == None"


def test_query_fields_and_protocol():
    query = And(Eq(Field("a"), 1), Not(Or(Field("b"), Field("a"))))
    assert query_fields(query) == frozenset({"a", "b"})
    assert field_name(Field("x")) == "x"


def test_unknown_node():
    with pytest.raises(AssertionError):
        eval_query("ne zapyt", RECORD)
    with pytest.raises(AssertionError):
        render_query(42)

from typing import Any, Mapping, Sequence, assert_never

from model import Or, HasName, Not, Field, Query, Eq, And


def eval_query(query: Query, record: Mapping[str, Any]) -> bool:
    match query:
        case Field(name):
            return bool(record.get(name, False))
        case Eq(field, value):
            return field.name in record and record[field.name] == value
        case And(left, right):
            return eval_query(left, record) and eval_query(right, record)
        case Or(left, right):
            return eval_query(left, record) or eval_query(right, record)
        case Not(inner):
            return not eval_query(inner, record)
        case _:
            assert_never(query)


def filter_records(query: Query, records: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return [record for record in records if eval_query(query, record)]


def field_name(obj: HasName) -> str:
    return obj.name


def query_fields(query: Query) -> frozenset[str]:
    match query:
        case Field():
            return frozenset({field_name(query)})
        case Eq(field, _):
            return frozenset({field_name(field)})
        case And(left, right) | Or(left, right):
            return query_fields(left) | query_fields(right)
        case Not(inner):
            return query_fields(inner)
        case _:
            assert_never(query)

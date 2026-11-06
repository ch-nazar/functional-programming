from evaluator import eval_query, query_fields, filter_records
from model import Or, Not, Field, Eq, And
from pretty import render_query

RECORDS = [
    {"nazva": "Zadacha 1", "status": "open", "priorytet": 1, "terminova": True},
    {"nazva": "Zadacha 2", "status": "closed", "priorytet": 2, "terminova": False},
    {"nazva": "Zadacha 3", "status": "open", "priorytet": 3, "terminova": False},
]

if __name__ == "__main__":
    query = And(Eq(Field("status"), "open"), Or(Field("terminova"), Not(Eq(Field("priorytet"), 3))))
    print("Zapyt:", render_query(query))
    print("Polya:", sorted(query_fields(query)))
    for record in RECORDS:
        print(record["nazva"], "->", eval_query(query, record))
    print("Pidkhodyat:", [record["nazva"] for record in filter_records(query, RECORDS)])

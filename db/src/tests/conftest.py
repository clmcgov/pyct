from os import environ

from psycopg2 import connect
from pytest import fixture, yield_fixture


@yield_fixture
def db():
    db = connect(
        host="localhost",
        dbname="test",
        user="test",
        password="test"
    )
    with db.cursor() as crsr:
        for sql in ("schema/germ.sql", "tests/data/germ.sql"):
            with open(sql, "r") as f:
                crsr.execute(f.read())
    db.commit()
    yield db
    db.close()


@yield_fixture
def bb():
    db = connect(
        host="localhost",
        dbname="test",
        user="test",
        password="test"
    )
    with db.cursor() as crsr:
        for sql in ("schema/germ.sql", "tests/data/baskin.sql"):
            with open(sql, "r") as f:
                crsr.execute(f.read())
    db.commit()
    yield db
    db.close()


@yield_fixture
def crsr(db):
    crsr = db.cursor()
    yield crsr
    crsr.close()
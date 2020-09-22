from textwrap import dedent

from psycopg2.errors import (
    UniqueViolation, NotNullViolation, CheckViolation, ForeignKeyViolation,
    RaiseException
)
from pytest import mark, raises

def test_baskin(bb):
    pass


'''
def _test_foo(crsr):
    crsr.execute("select * from germ_result")
    assert crsr.fetchall() == []


def test_germ_method(crsr):
    crsr.execute("select * from germ_method(1)")
    assert crsr.fetchall() == [([1, 2, 4],), ([1, 2, 3, 5],)]


@mark.parametrize("vals", [
    "1, 10, 11",
    "3, 12, 5"
])
def test_insert_germ_count(crsr, vals):
    with raises(RaiseException):
        crsr.execute(dedent(f"""\
            insert into germ_count
                (treatment_id, count_day, germinated)
            values
                ({vals});
            """
        ))


def test_update_germ_transfer(crsr):
    with raises(RaiseException):
        crsr.execute(dedent("""\
            update germ_transfer
            set target_id = 1
            where target_id = 3
            """
        ))


@mark.parametrize("args,rets", [
    ("1",       [(1, 5, 4, 1), (2, 0, None, 0), (3, 4, None, 4), (4, 1, None, 1), (5, 0, None, 0)]),
    ("1, 12",   [(1, 5, 4, 1), (2, 1, None, 1), (3, 4, None, 4)]),
    ("1, 10",   [(1, 10, None, 10)])
])
def test_germ_status(crsr, args, rets):
    crsr.execute(dedent(f"""\
        select * from germ_status({args});
        """
    ))
    assert crsr.fetchall() == rets


def test_update_germ_moisture(crsr):
    crsr.execute(dedent("""\
        update germ_moisture
        set name = 'foo'
        where name = 'H2O';
        """
    ))
    crsr.execute(dedent("""\
        select distinct moisture
        from germ_treatment;
        """
    ))
    assert crsr.fetchone()[0] == 'foo'


def test_delete_germ_treatment(crsr):
    """cascade delete to transfers, trigger after transfer
    """
    with raises(RaiseException) as e:
        crsr.execute(dedent("""\
            delete from germ_treatment 
            where id = 1;
            """
        ))
    assert "after_germ_transfer_del" in e.value.pgerror


def test_delete_germ_transfer(crsr):
    """causes negative seed count for treatment 2
    """
    with raises(RaiseException):
        crsr.execute(dedent("""\
            delete from germ_transfer 
            where source_id = 1 and target_id = 2;
            """
        ))


@mark.parametrize("vals", [
    "1, 3, 4, 100", # negative seed
    "1, 2, 1, 0",   # time travel
    "1, 1, 6, 0",   # transfer to control
    "1, 6, 3, 0"    # transfer from control
])
def test_insert_germ_transfer(crsr, vals):
    """
    """
    with raises(RaiseException):
        crsr.execute(dedent(f"""\
            insert into germ_transfer
                (test_id, source_id, target_id, seed_number)
            values
                ({vals})
            """
        ))



def test_update_treatment_control(crsr):
    """try to create cycles
    """
    with raises(RaiseException):
        crsr.execute(dedent(f"""\
            update germ_treatment
            set
                control = true
            where
                id = 1
            """
        ))


@mark.parametrize("treatmentId,sDay", [
    (3, 9),     # terminal starts before initial
    (2, 9),     # child starts before parent
    (3, 10),    # terminal starts at same time as parent
    (2, 10)     # child starts at same time as parent  
])
def test_update_treatment_start(crsr, treatmentId, sDay):
    """try to create cycles
    """
    with raises(RaiseException):
        crsr.execute(dedent(f"""\
            update germ_treatment
            set
                start_day = {sDay}
            where
                id = {treatmentId}
            """
        ))
'''
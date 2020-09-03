from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal
from os import environ
from pdb import set_trace
from sqlite3 import (
    PARSE_DECLTYPES, connect, register_adapter, register_converter
)
from textwrap import dedent

from clr import AddReference
AddReference("System")
AddReference("cs/PyCT/bin/Debug/PyCT")
from System import DBNull, DateTime, Decimal as Decimal_
from PyCT import Adapter

# for table creation
DTYPES = {
    "Boolean": "boolean",
    #"Byte": ,
    #"Char": ,
    "DateTime": "timestamp",
    "Decimal": "decimal",
    "Double": "real",
    #"Guid": ,
    "Int16": "integer",
    "Int32": "integer",
    "Int64": "integer",
    #"SByte": ,
    #"Single": ,
    "String": "text",
    #"TimeSpan": ,
    "UInt16": "integer",
    "UInt32": "integer",
    "UInt64": "integer"
}

GRIN_URL = environ.get("GRIN_URL")

# decimal dtype
def adapt_decimal(val):
    return str(val)

def convert_decimal(val):
    return Decimal(val.decode())

register_adapter(Decimal, adapt_decimal)
register_converter("decimal", convert_decimal)

# boolean dtype
def adapt_boolean(val):
    return int(val)

def convert_boolean(val):
    return bool(val)

register_adapter(bool, adapt_boolean)
register_converter("boolean", convert_boolean)


class Session:

    """communicates with GG middle tier
    """

    def __init__(self, username, password, url=GRIN_URL):
        """create .net adapter object and temporary SQLite db
        """
        # create .net object in clr, get wrapper
        self._service = Adapter(username, password, url)
        # create unique temp db for this connection
        self._db = connect("", detect_types=PARSE_DECLTYPES)

    def __enter__(self):
        # connection already open
        return self

    def __exit__(self, *args):
        self.end()

    def __del__(self):
        self.end()

    @property
    def db(self):
        return self._db

    def end(self):
        """close db connection and drop
        """
        # close connection (drops temp db)
        self._db.close()

    def add_data(self, dataview, offset=0, limit=0, params={}):
        """populate temp db with data from dataview
        """
        params = self._param_string(params)
        # get .net dataset and table of interest
        ds = self._service.GetData(dataview, params, offset, limit)
        dt = ds.Tables[dataview]
        # get list of (column name, dtype)
        cols = [(c.ToString(), c.DataType.get_Name()) for c in dt.Columns]
        self._create_table(dataview, cols)
        self._insert_rows(dataview, cols, dt.Rows)
        # make sure memory freed up (who knows what .net is doing)
        dt.Clear()
        dt.Dispose()

    def _create_table(self, name, columns):
        """create table in tmp db from datatable if it doesn't exist
        """
        cols = ", ".join(f"{c[0]} {DTYPES[c[1]]}" for c in columns) 
        self.db.execute(f"create table if not exists {name} ({cols});")
        self.db.commit()

    def _insert_rows(self, table, columns, rows):
        """insert rows from datatable
        """
        cols = ",".join("?" * len(columns))
        sql = f"insert into {table} values ({cols})"
        gen = (self._to_record(r) for r in rows)
        # automatic begin transaction
        self.db.executemany(sql, gen)
        self.db.commit()

    @staticmethod
    def _to_record(row):
        """convert System.DataRow to tuple
        """
        res = []
        for val in row.get_ItemArray():
            if isinstance(val, DBNull):
                res.append(None)
            elif isinstance(val, DateTime):
                tmp = datetime(val.Year, val.Month, val.Day, val.Hour, val.Minute, val.Second)
                res.append(tmp)
            elif isinstance(val, Decimal_):
                res.append(Decimal(val.ToString()))
            else:
                res.append(val)
        return tuple(res)

    @staticmethod
    def _param_string(params):
        """convert dict of params to CSS-style string
        """
        res = []
        for key, val in params.items():
            tmp = f":{key}="
            # if it's some kind of collection that's not a string or bytes
            if hasattr(val, "__iter__") and not isinstance(val, (str, bytes)):
                tmp += ",".join(str(x) for x in val)
            else:
                try:
                    #try to decode it if it's bytes
                    val = val.decode('utf16')
                except AttributeError:
                    pass
                # just use as is if it can't be decoded
                tmp += str(val)
            res.append(tmp)
        return ";".join(res)

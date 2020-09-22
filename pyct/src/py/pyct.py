from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal
from os import environ as env
from pdb import set_trace
from sqlite3 import (
    PARSE_DECLTYPES, connect, register_adapter, register_converter
)
from textwrap import dedent

from clr import AddReference
AddReference("System")
AddReference("../cs/PyCT/bin/Debug/PyCT")
from System import DBNull, DateTime, Decimal as Decimal_
from PyCT import Adapter

# for table creation (all supported .NET dataTable dtypes) 
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

    def __init__(self, username=None, password=None, url=None):
        """create .net adapter object and temporary SQLite db
        """
        # create .net object in clr, get wrapper
        self._adapter = Adapter(
            username=username or env["GRIN_USER"], 
            password=password or env["GRIN_PASSWORD"], 
            url=url or env["GRIN_URL"]
        )
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
        self._adapter = None

    def validate(self):
        """validate login, return dict of user info
        """
        ds = self._adapter.Validate()
        dt = ds.Tables['validate_login']
        keys = [str(c) for c in dt.Columns]
        vals = self._to_record(dt.Rows[0])
        return dict(zip(keys, vals))

    def add_data(self, dataView, parms=None, offset=0, limit=0):
        """populate temp db with data from dataView
        create empty table if no rows are returned
        """
        parms = self._to_parm_string(parms) if parms else ""
        # get .net dataset and table of interest
        ds = self._adapter.GetData(dataView, parms, offset, limit)
        dt = ds.Tables[dataView]
        self._create_table(dt)
        if dt.Rows.Count:
            self._insert_rows(dt)
        # try to free up memory (who knows what .net is doing)
        dt.Clear()
        dt.Dispose()

    def save_data(self, dataView, select):
        # get empty table
        ds = self._adapter.GetData(dataView, "", 0, 0)
        dt = ds.Tables[dataView]
        # then iterate over rows from select and add to ds

    def _create_table(self, dataTable):
        """create table in tmp db from dataTable if it doesn't exist
        """
        # get dtype and generate sql
        name = dataTable.TableName
        cols = ", ".join(
            f"{str(c)} {DTYPES[c.DataType.Name]}" 
            for c in dataTable.Columns
        ) 
        self.db.execute(f"create table if not exists {name} ({cols});")
        self.db.commit()

    def _insert_rows(self, dataTable):
        """insert rows from dataTable
        """
        name = dataTable.TableName
        cols = ",".join("?" * len(dataTable.Columns.Count))
        rows = dataTable.Rows
        sql = f"insert into {name} values ({cols})"
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
                tmp = datetime(
                    val.Year, val.Month, val.Day, val.Hour, val.Minute, 
                    val.Second
                )
                res.append(tmp)
            elif isinstance(val, Decimal_):
                res.append(Decimal(val.ToString()))
            else:
                res.append(val)
        return res

    @staticmethod
    def _to_parm_string(parms):
        """convert dict of parms to CSS-style string
        """
        res = []
        for key, val in parms.items():
            res.append(f":{key}=" + ",".join(str(x) for x in val))
        return ";".join(res)

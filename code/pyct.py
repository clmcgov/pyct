
from clr import AddReference
from datetime import datetime
from decimal import Decimal

AddReference("System")
AddReference("cs/PyCT/bin/Debug/PyCT")

from System import DBNull as _DBNull, DateTime as _DateTime, Decimal as _Decimal
from PyCT import Adapter

DEV = "https://npgsdev.ars-grin.gov/GRINGlobal/GUI.asmx"
WEB = "https://npgsweb.ars-grin.gov/GRINGlobal/GUI.asmx" 

class Service:

    """communicates with GG middle tier
    """

    def __init__(self, username, password, url=DEV):
        self._service = Adapter(username, password, url)
    
    def get_data(self, table, offset=0, limit=0, **or_):
        """get a Table object wrapping the underlying System.DataTable 

        Parameters
        ----------
        table : str
            name of table (dataview)
        offset : int
            number of rows to skip
        limit : int
            number of rows to return
        or_
            arbitrary key word arguments specifying OR equality conditions
            on dataview parameters
            ex: get_data(..., foo=1, bar=["baz", "qux"]) 
                -> foo=1 OR bar IN ("baz", "qux")

        Returns
        -------
        pyct.Table
        """
        params = self._param_string(or_)
        ds = self._service.GetData(table, params, offset, limit)
        return Table(ds.Tables[table])

    def get_params(self, table):
        """get valid parameters for a table (dataview)

        Parameters
        ----------
        table : str
            name of table (dataview)

        Returns
        -------
        list
        """
        tbl = self.get_data("get_dataview_parameters", dataview=table)
        return tbl.columns[:2], [r[:2] for r in tbl]

    @property
    def tables(self):
        """available tables (dataviews)
        """
        tbl = self.get_data("sys_dataview")
        cols = tbl.columns
        return [cols[1], cols[6]], [(r[1], r[6]) for r in tbl]

    @staticmethod
    def _param_string(params):
        """convert dict of params to CSS-style string
        """
        res = []
        for key, val in params.items():
            tmp = f":{key}="
            if isinstance(val, (list, tuple)):
                tmp += ",".join(str(x) for x in val)
            else:
                tmp += str(val)
            res.append(tmp)
        return ";".join(res)


class Table:
    
    """indexable iterable of rows, wraps System.DataTable result from MT
    """

    def __init__(self, dotNetDataTable):
        self._dataTable = dotNetDataTable

    def __getitem__(self, row):
        return self._to_record(self._dataTable.Rows[row])

    def __len__(self):
        return self._dataTable.Rows.Count

    def __iter__(self):
        for row in self._dataTable.Rows:
            yield self._to_record(row)

    @property
    def columns(self):
        """columns of this table
        """
        return [str(c) for c in self._dataTable.Columns]

    @staticmethod
    def _to_record(row):
        """convert System.DataRow to tuple
        """
        res = []
        for val in row.get_ItemArray():
            if isinstance(val, _DBNull):
                res.append(None)
            elif isinstance(val, _DateTime):
                tmp = datetime(val.Year, val.Month, val.Day, val.Hour, val.Minute, val.Second)
                res.append(tmp)
            #elif isinstance(val, _Decimal):
            #    res.append(Decimal(val))
            else:
                res.append(val)
        return tuple(res)
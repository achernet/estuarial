import collections
import datetime as dt
from arraymanagement.nodes.csvnodes import PandasCSVNode
from arraymanagement.nodes.hdfnodes import PandasHDFNode
from arraymanagement.nodes.sql import SimpleQueryTable
from arraymanagement.nodes.sqlcaching import (DumbParameterizedQueryTable, 
                                              BulkParameterizedQueryTable,
                                              FlexibleSqlCaching
                                              )
import pyodbc
creds = {
    "Uid": "qas_test",
    "Pwd": "qasqasqas",
}
sql_alchemy_conn = "mssql+pyodbc://qas_test:qasqasqas@tdstest"
connstring = 'DSN=tdstest;UID=%s;PWD=%s'%(creds['Uid'],creds['Pwd'])
global_config = dict(
    is_dataset = False,
    csv_options = {},
    datetime_type = 'datetime64[ns]',
    db_module = pyodbc,
    db_conn_args = (connstring,),
    db_conn_kwargs = {},
    sqlalchemy_args = [sql_alchemy_conn],
    sqlalchemy_kwargs = {},
    col_types = {},
    min_itemsize = {},
    db_string_types = [str],
    db_datetime_types = [dt.date, dt.datetime],
    loaders = {
        '*.csv' : PandasCSVNode,
        '*.CSV' : PandasCSVNode,
        '*.hdf5' : PandasHDFNode,
        '*.h5' : PandasHDFNode,
        '*.sql' : SimpleQueryTable,
        "*.sqlspec" : DumbParameterizedQueryTable,
        "*.bsqlspec" : BulkParameterizedQueryTable,
        "*.fsql" : FlexibleSqlCaching
        },
    )            

local_config = {}

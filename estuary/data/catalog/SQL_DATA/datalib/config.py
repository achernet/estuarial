import collections
import os
import datetime as dt
from arraymanagement.nodes.csvnodes import PandasCSVNode
from arraymanagement.nodes.hdfnodes import PandasHDFNode
from arraymanagement.nodes.sql import SimpleQueryTable
from arraymanagement.nodes.sqlcaching import (DumbParameterizedQueryTable, 
                                              BulkParameterizedQueryTable,
                                              FlexibleSqlCaching,
                                              MetaSqlCaching,
                                              FlexibleSqlDateCaching,
                                              )
import pyodbc
from estuary.config import Config
config = Config()

username = config.get('ESTUARY','UserName')
passwd   = config.get('ESTUARY','Password')
db   = config.get('ESTUARY','Database')
server   = config.get('ESTUARY','Server')
port   = config.get('ESTUARY','Port')
driver   = config.get('ESTUARY','Driver')

if os.name == 'nt':
    sql_alchemy_conn = "mssql+pyodbc://%s:%s@%s/%s"%(username,passwd,server,db)
    connstring = 'Driver=%s;Database=%s;Server=%s;Port=%s;UID=%s;PWD=%s'%(driver,db,server,port,\
                                                                            username,passwd)

else:   
    sql_alchemy_conn = "mssql+pyodbc://%s:%s@estuary"%(username,passwd)
    connstring = 'DSN=estuary;UID=%s;PWD=%s'%(username,passwd)

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
        "*.fsql" : FlexibleSqlCaching,
        "*.msql" : MetaSqlCaching,
        "*.fdsql": FlexibleSqlDateCaching,
        },
    cache_dir = '~/.estuary/',
    )            

local_config = {}

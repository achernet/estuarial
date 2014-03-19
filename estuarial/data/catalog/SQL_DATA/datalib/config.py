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
from estuarial.util.config import Config
config = Config()

username = config.get('ESTUARIAL','UserName')
passwd   = config.get('ESTUARIAL','Password')
db   = config.get('ESTUARIAL','Database')
server   = config.get('ESTUARIAL','Server')
port   = config.get('ESTUARIAL','Port')
driver   = config.get('ESTUARIAL','Driver')


if os.name == 'nt':
    sql_alchemy_conn = "mssql+pyodbc://%s:%s@%s/%s"%(username,passwd,server,db)
    connstring = 'Driver=%s;Database=%s;Server=%s;Port=%s;UID=%s;PWD=%s'%(driver,db,server,port,\
                                                                            username,passwd)

else:
    sql_alchemy_conn = "mssql+pyodbc://%s:%s@estuarial"%(username,passwd)

    #check if using FREETDS
    version = config.get('ESTUARIAL','TDS_VERSION')
    if version:
        connstring = 'Driver=%s;Server=%s;Database=qai;Uid=%s;Pwd=%s;TDS_VERSION=8.0;PORT=%s'%(driver, \
                             server,username,passwd,port)
    else:
        connstring = 'DSN=estuarial;UID=%s;PWD=%s'%(username,passwd)

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
    cache_dir = '~/.estuarial/',
    )

local_config = {}

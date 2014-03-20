import os
import pyodbc
import collections
import datetime as dt
from estuarial.util.config import Config
from arraymanagement.nodes.sql import SimpleQueryTable
from arraymanagement.nodes.csvnodes import PandasCSVNode
from arraymanagement.nodes.hdfnodes import PandasHDFNode
from arraymanagement.nodes.sqlcaching import (DumbParameterizedQueryTable,
                                              BulkParameterizedQueryTable,
                                              FlexibleSqlCaching,
                                              MetaSqlCaching,
                                              FlexibleSqlDateCaching)

config = Config()
port = config.get('ESTUARIAL', 'Port')
db = config.get('ESTUARIAL', 'Database')
server = config.get('ESTUARIAL', 'Server')
driver = config.get('ESTUARIAL', 'Driver')
passwd = config.get('ESTUARIAL', 'Password')
username = config.get('ESTUARIAL', 'UserName')

if os.name == 'nt':
    sql_alchemy_conn = "mssql+pyodbc://{}:{}@{}/{}".format(username,
                                                           passwd,
                                                           server,
                                                           db)

    connstring = 'Driver={};Database={};Server={};Port={};UID={};PWD={}'.format(
        driver,
        db,
        server,
        port,
        username,
        passwd)

else:
    sql_alchemy_conn = "mssql+pyodbc://{}:{}@estuarial".format(username, 
                                                               passwd)

    # if FreeTDS
    version = config.get('ESTUARIAL', 'TDS_VERSION')
    if version:
        connstring = ('Driver={};Server={};Database=qai;Uid={};Pwd={};'
                      'TDS_VERSION=8.0;PORT={}').format(driver,
                                                        server,
                                                        username,
                                                        passwd,
                                                        port)
    else:
        connstring = 'DSN=estuarial;UID={};PWD={}'.format(username, passwd)

global_config = dict(is_dataset=False,
                     csv_options={},
                     datetime_type='datetime64[ns]',
                     db_module=pyodbc,
                     db_conn_args=(connstring,),
                     db_conn_kwargs={},
                     sqlalchemy_args=[sql_alchemy_conn],
                     sqlalchemy_kwargs={},
                     col_types={},
                     min_itemsize={},
                     db_string_types=[str],
                     db_datetime_types=[dt.date, dt.datetime],
                     loaders={'*.csv':PandasCSVNode,
                              '*.CSV':PandasCSVNode,
                              '*.hdf5':PandasHDFNode,
                              '*.h5':PandasHDFNode,
                              '*.sql':SimpleQueryTable,
                              "*.sqlspec":DumbParameterizedQueryTable,
                              "*.bsqlspec":BulkParameterizedQueryTable,
                              "*.fsql":FlexibleSqlCaching,
                              "*.msql":MetaSqlCaching,
                              "*.fdsql": FlexibleSqlDateCaching},
                     cache_dir = '~/.estuarial/')

local_config = {}

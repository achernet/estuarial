import pandas
import pyodbc
import os
import re
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, event
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.engine import Engine
import json
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection


class SQLServerDataSource():
    """ Class for connecting to, and manipulating a SQL database instance """
    
    def __init__(self, rootDir=None):
        """ rootDir: root directory for a SQLServerDataSource config layout on disk"""
        
        self.rootDir = rootDir
        config_filepath = rootDir + '/' + os.path.basename(rootDir) + '.json'
            
        try:
            config = json.load(open(config_filepath))
        except:
            raise Exception("error loading %s " % config_filepath)
                
        try:
            conn = config['connection'] 
            print 'connecting to MSSQL Database'
            
            conn_string = 'mssql+pyodbc://%s:%s@%s:%s/qai' % (conn['username'], conn['password'], conn['server'], conn['port'])
            print(conn_string)
            
            self.db_engine = create_engine(conn_string)
        except:
            raise Exception("Error connecting to TR Database.  Please makes sure you are using a json dictionary\nwith valid driver,server,Uid,and Pwd defined.")
        
        self.db_session = sessionmaker(bind=self.db_engine)()
        
        self.metadata = MetaData(bind = self.db_engine)
        self.conn = self.db_engine.connect()
        
        self.db_object_suffix = config['db_object_suffix']
        self.schema = config['writeable_schema']
        
        def fix_sql(sql):
            """ Returns a cleaned version of sqlRaw with correct version suffix """
            sql = re.sub('%s\\.(\\w*)' % self.schema, r'%s.\1' % self.schema + self.db_object_suffix, sql) #.replace('\n',' ')
#            print(sql)
            return sql           
            
        self.fix_sql = fix_sql
        
        def engine_fix_sql(conn, cursor, statement, parameters, context, executemany):
            statement = fix_sql(statement)
            return statement, parameters
        
        event.listen(self.db_engine, "before_cursor_execute", engine_fix_sql)
        
        self.config = config

    def __execute(self, sqlRaw):
        """ convenience method for executing sql commands that return nothing """
        trans = self.conn.begin()
        self.conn.execute(self.fix_sql(sqlRaw))
        trans.commit()
        
    def create_view(self, name, sql):
        """ create a view object """
        sql = "CREATE VIEW " + name + " AS " + sql
        self.__execute(sql)
    
    def drop_and_create_view(self, name, sql):
        """ drop if exists and create the view either way """
        
        trans = self.conn.begin()
        dropIfExists = """
                            IF  EXISTS (SELECT * FROM sys.views WHERE object_id = OBJECT_ID(N'%s'))
                            DROP VIEW %s
                        """ % (name, name)
        self.__execute(dropIfExists)
        trans.commit()
        self.create_view(name, sql)
        
    def create_proc(self, name, params, body):
        """ create a stored procedure object """
        sql = "CREATE PROCEDURE " + name + " " + params + " AS " + body
        self.__execute(sql)

    def drop_and_create_proc(self, name, params, body):
        """ drop if exists and create the stored procedure either way """
        
        trans = self.conn.begin()
        dropIfExists = """
                            IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'%s') AND type IN (N'P, N'PC'))
                            DROP PROCEDURE %s
                        """ % (name, name)
        self.__execute(dropIfExists)
        trans.commit()
        self.create_proc(name, params, body)
    
    def create_scalar_function(self, name, params, return_type, body):
        """ create a scalar-valued function object """
        sql = "CREATE FUNCTION " + name + " (" + params + ") RETURNS " + return_type + " AS " + body
        self.__execute(sql)
        
    def drop_and_create_scalar_function(self, name, params, return_type, body):
        """ drop if exists and create the scalar-valued function either way """
        
        trans = self.conn.begin()
        dropIfExists = """
                            IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'%s') AND type IN (N'FN', N'IF', N'TF', N'FS', N'FT'))
                            DROP FUNCTION %s
                        """ % (name, name)
        self.__execute(dropIfExists)
        trans.commit()
        self.create_scalar_function(name, params, body)
    
    def add_content_set(self, content_set):
        pass
    
    @property
    def content_sets(self):
        return self._content_sets
    
    @property
    def managed_views(self):
        return self._managed_views
    
    @property
    def managed_procs(self):
        return self._managed_procs
    
    @property
    def entities(self):
        return self._entities
    
    @property
    def metrics(self):
        return self._metrics
    


#class QADMappedSource():
#    __ventype__ = None
#    pass
#    
#    
#class EntitySource():
#    pass
#
#class TimeSeriesSource():
#    pass
#
#class EAVSource():
#    pass
#
#class BiTemporalSource():
#    pass
#
#class EstimatesSource(BiTemporalSource):
#    pass
#
#class FinancialStatementSource(BiTemporalSource):
    pass


Base = declarative_base(cls=DeferredReflection)

class TableDataSource(object):
    
    @property
    def table(self):
        return self._table
    
    
    
    def __init__(self, tablespec, metadata, autoload=True):
        self.__tablespec = tablespec
        self._metadata = metadata
        self._tablename = tablespec['name']
        self._schema = tablespec['schema']
        
        
        metadata.reflect(only=[self._tablename],schema=self._schema,views=True)
        
        self._table = metadata.tables[self._schema + '.' + self._tablename]

                
        #set column aliases
        for alias, name in tablespec['column_aliases'].items():
            self._table.columns[name].key = alias
        
        #add primary key columns
        self._pkey_column = self._table.columns[tablespec['primary_key']]
        self._pkey_column.primary_key = True
            
            
    def query_all(self, session):
        '''builds and executes a query 
         returns a dataframe containing all available data from this table'''
        q = session.query(self.table)
        return q
        
        
    def query_with_ids(self, session, ids):
        '''returns a query object that will fetch all available data from this table
            filtered by a list of ids.
        '''
        q = session.query(self.table)
        q = q.filter(self._pkey_column.in_(ids))
        return q
    
        


def query_todataframe(query):
    return pandas.DataFrame.from_records(map(
                                    lambda x:x.__dict__, 
                                    query.all())
                                    )
    
      
    
if __name__ == "__main__":
    os.chdir('..')
    s = SQLServerDataSource('./data_sources/qadirect')
                                        
    ds2 = json.load(open('./table_specs/DS2.json'))
    ds2primqt = ds2['Ds2PrimQt']
    ds2eqmstr = ds2['DS2EqMstr']

    rkd = json.load(open('./table_specs/RKD.json'))
    rkd = rkd['RKD_Fundamentals']

    ds2primqt_tb = TableDataSource(ds2primqt, s.metadata)
    ds2eqmstr_tb = TableDataSource(ds2eqmstr, s.metadata)
    rkd_tb = TableDataSource(rkd, s.metadata)

    qtd = query_todataframe

    q = ds2eqmstr_tb.query_all(ses)

    #df = qtd(q.limit(12))

    

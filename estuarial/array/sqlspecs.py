from os.path import join, relpath
import pandas as pd
from pandas.io import sql
from arraymanagement.nodes.hdfnodes import (write_pandas,
                                            override_hdf_types,
                                            write_pandas_hdf_from_cursor
                                            )
from arraymanagement.nodes.sql import query_info
from arraymanagement.nodes.sqlcaching import YamlSqlDateCaching

from sqlalchemy.sql import column, and_


from arraymanagement.logger import log

import yaml
from copy import deepcopy

BATCH_SIZE = 8000


class QADirectSqlCaching(YamlSqlDateCaching):
    def init_from_file(self):
        with open(join(self.basepath, self.relpath)) as f:
            data = yaml.load(f)
            assert len(data['SQL'].keys()) == 1

            key = data['SQL'].keys()[0]
            query = data['SQL'][key]['query']
            if 'conditionals' in data['SQL'][key].keys():
                fields = data['SQL'][key]['conditionals']
            else:
                fields = None

            if 'ventype' in data['SQL'][key].keys():
                self.codetype = data['SQL']['codetype']
            if 'code_column' in data['SQL'][key].keys():
                self.code_column = data['SQL'][key]['code_column']

            self.query = query
            self.fields = fields

            #no conditionals defined
            if fields is not None:
                for f in fields:
                    name = f.lower()
                    setattr(self, name, column(name))

    def cache_data(self, query_params, start_date, end_date):

        for f in self.fields:
            if 'date' in f:
                col_date = f
                break;

        all_query = and_(query_params,column(col_date) >=start_date, column(col_date) <= end_date)
        q = self.cache_query(all_query)
        log.debug(str(q))

        min_itemsize = self.min_itemsize if self.min_itemsize else {}
        db_string_types = self.db_string_types if self.db_string_types else []
        db_datetime_types = self.db_datetime_types if self.db_datetime_types else []

        self.min_itemsize = min_itemsize
        self.finalize_min_itemsize()
        overrides = self.col_types

        # get code clause index
        code_index = None
        for i in range(0, len(q.whereclause.clauses)):
            if hasattr(q.whereclause.clauses[i], 'clauses'):
                if str(q.whereclause.clauses[i].clauses[0].left) == self.code_column:
                    code_index = i
                    codes = [x.effective_value for x in q.whereclause.clauses[0].clauses[0].right.element.clauses]
                    break
            else:
                if str(q.whereclause.clauses[i].left) == self.code_column:
                    code_index = i
                    codes = [x.effective_value for x in q.whereclause.clauses[0].right.element.clauses]
                    break

        df_out = None

        # get list of codes
        # codes = [x.effective_value for x in q.whereclause.clauses[0].clauses[0].right.element.clauses]
        total_elements = len(codes)

        # open transaction
        #create temp table and insert codes
        self.session.execute("if exists (select 1 where object_id('tempdb.dbo.#tmp') is not null) drop table #tmp")
        self.session.execute("create table #tmp (id int)")
        self.session.execute("create clustered index IX on #tmp(id)")
        for i in range(0, int(round(total_elements / float(BATCH_SIZE) + 1))):
            start = i * BATCH_SIZE
            end = start + BATCH_SIZE - 1
            if start >= total_elements:
                break
            if end >= total_elements:
                end = total_elements - 1
            insert = "insert into #tmp select * from trqa.CSVToTable('%s',',')" % ','.join([str(x) for x in codes[start:end]])
            self.session.execute(insert)

        #modify query object to use temp table instead of IN()
        q.whereclause.clauses = (q.whereclause.clauses[:code_index] + q.whereclause.clauses[(code_index + 1):])
        filter_codes = "%s IN (select id from #tmp)" % self.code_column

        #execute query with substituted filter
        cur = self.session.execute(q.filter(filter_codes))

        cur.description = cur._cursor_description()
        cur.arraysize = 500

        columns, min_itemsize, dt_fields = query_info(
            cur,
            min_itemsize=min_itemsize,
            db_string_types=db_string_types,
            db_datetime_types=db_datetime_types
            )
        self.min_itemsize = min_itemsize
        self.finalize_min_itemsize()
        overrides = self.col_types
        for k in dt_fields:
            overrides[k] = 'datetime64[ns]'
        try:
            starting_row = self.table.nrows
        except AttributeError:
            starting_row = 0

        write_pandas_hdf_from_cursor(self.store, self.localpath, cur,
                                     columns, self.min_itemsize,
                                     dtype_overrides=overrides,
                                     min_item_padding=self.min_item_padding,
                                     chunksize=500000,
                                     replace=False)
        try:
            ending_row = self.table.nrows
        except AttributeError:
            ending_row = 0
        self.store_cache_spec(query_params, starting_row, ending_row, start_date, end_date)

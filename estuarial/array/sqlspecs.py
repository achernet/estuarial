from os.path import join, relpath
import pandas as pd
from pandas.io import sql
from arraymanagement.nodes.hdfnodes import (get_pandas_from_cursor,
                                            write_pandas,
                                            override_hdf_types,
                                            )
from arraymanagement.nodes.sql import query_info
from arraymanagement.nodes.sqlcaching import YamlSqlDateCaching

from sqlalchemy.sql import column, and_


from arraymanagement.logger import log

import yaml
from copy import deepcopy

BATCH_SIZE = 2050


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
                self.key_column = data['SQL']['key_column']

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

        total_elements = len(q.whereclause.clauses[0].clauses[0].right.element.clauses)
        min_itemsize = self.min_itemsize if self.min_itemsize else {}
        db_string_types = self.db_string_types if self.db_string_types else []
        db_datetime_types = self.db_datetime_types if self.db_datetime_types else []

        self.min_itemsize = min_itemsize
        self.finalize_min_itemsize()
        overrides = self.col_types


        try:
            starting_row = self.table.nrows
        except AttributeError:
            starting_row = 0

        df_out = None
        # HACK: dt_fields will definitely be the same for each batch here, so just use the last one
        dt_fields = None
        clauses = deepcopy(q.whereclause.clauses[0].clauses[0].right.element.clauses)
        for i in range(0, int(round(total_elements / float(BATCH_SIZE) + 1))):
            start = i * BATCH_SIZE
            end = start + BATCH_SIZE - 1
            if start >= total_elements:
                break
            if end >= total_elements:
                end = total_elements - 1

            # create a query with only the current batch of elements
            q.whereclause.clauses[0].clauses[0].right.element.clauses = clauses[start:end]


            cur = self.session.execute(q)

            #hack
            cur.description = cur._cursor_description()
            cur.arraysize = 500


            columns, min_itemsize, dt_fields = query_info(
                cur,
                min_itemsize=min_itemsize,
                db_string_types=db_string_types,
                db_datetime_types=db_datetime_types
                )

            for k in dt_fields:
                overrides[k] = 'datetime64[ns]'

            df = get_pandas_from_cursor(cur,
                                     columns, self.min_itemsize,
                                     dtype_overrides=overrides,
                                     min_item_padding=self.min_item_padding,
                                     chunksize=50000,
                                     replace=False)
            if df_out is None:
                df_out = df
            else:
                df_out.append(df)

        try:
            starting_row = self.table.nrows
        except AttributeError:
            starting_row = 0

        df_out = override_hdf_types(df_out, overrides)
        write_pandas(self.store, self.localpath, df_out,
                                     self.min_itemsize,
                                     min_item_padding=self.min_item_padding,
                                     chunksize=50000,
                                     replace=False)
        try:
            ending_row = self.table.nrows
        except AttributeError:
            ending_row = 0
        self.store_cache_spec(query_params, starting_row, ending_row, start_date, end_date)

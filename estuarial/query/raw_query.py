from __future__ import print_function, division, absolute_import

from estuarial.array.arraymanagementclient import ArrayManagementClient
import pandas as pd

class RAW_QUERY(ArrayManagementClient):
    '''
    Functional style interface into TR's DB.  Most functions take 3 arguments:

    - Universe (list of entities)
    - Metrics (list of measurements)
    - Date Range

    '''

    def __init__(self):
        super(RAW_QUERY, self).__init__()

    def raw_query(self, sql=None):
        """
        Raw SQL Query

        :type query: string
        :param query: raw sql query

        """

        #just a random url (must be valid)
        url = '/FUNDAMENTALS/WORLDSCOPE/wsitems.yaml'
        arr = self.aclient[url]

        cur = arr.session.execute(sql)

        cur.description = cur._cursor_description()
        cols = [col[0] for col in cur.description]

        data = cur.fetchall()

        df = pd.DataFrame.from_records(data)
        df.columns = cols

        return df



# Kind of hate the spelling
# from estuarial.query.raw_query import RAW_QUERY
#
# rquery = RAW_QUERY()
# sql = '''
# select * from idxinfo where code in (select distinct idxcode from idxspcmp)
# '''
#
# rquery.raw_query(sql)

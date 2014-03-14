import datetime
from sqlalchemy.sql import column, and_, or_
from thomson.array.arraymanagementclient import ArrayManagementClient

# the supported metrics
def get_metrics_list():
    return [('ohlc', _OHLCIndexer),
            ('cash', _CASHIndexer),
            ('ni', _NIIndexer)]

class _TRUniverseIndexer(ArrayManagementClient):

    def __init__(self, obj, name):
        self.obj = obj
        self.name = name

    def _check_end(self,stop):
        '''[X:] results in the two following possibilities'''

        if stop == 9223372036854775807 or stop == None:
            now = datetime.datetime.utcnow().strftime('%Y-%m-%d')
            return now
        else:
            return stop

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = index.start
            stop = self._check_end(index.stop)
            return start, stop
        else:
            raise TypeError("index must be datetime slice")

class _OHLCIndexer(_TRUniverseIndexer):

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = index.start
            stop = self._check_end(index.stop)
            universe = self.obj.data.seccode.tolist()
            arr = self.obj.aclient['/DataStream/ohlc.fsql']
            ohlc = arr.select(and_(arr.seccode.in_(universe),
                                   arr.marketdate >= start,
                                   arr.marketdate <= stop))
            return ohlc
        else:
            raise TypeError("index must be datetime slice")

class _CASHIndexer(_TRUniverseIndexer):

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = index.start
            stop = self._check_end(index.stop)
            universe = self.obj.data.seccode.tolist()
            item = 2001 # cash
            freq = 'Q'  # Quarterly Maybe use step for this?
            ws_query_loc = '/WORLDSCOPE/worldscope_metrics_date_select.fsql'
            arr = self.obj.aclient[ws_query_loc]
            cash = arr.select(and_(arr.seccode.in_(universe),
                                   arr.item == item,
                                   arr.freq == freq,
                                   arr.fdate >= start,
                                   arr.fdate <= stop))
            return cash
        else:
            raise TypeError("index must be datetime slice")

class _NIIndexer(_TRUniverseIndexer):

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = index.start
            stop = self._check_end(index.stop)
            universe = self.obj.data.seccode.tolist()
            item = 1751 # net income
            freq = 'Q'  # Quarterly Maybe use step for this?
            ni_query_loc = '/WORLDSCOPE/worldscope_metrics_date_select.fsql'
            arr = self.obj.aclient[ni_query_loc]
            cash = arr.select(and_(arr.seccode.in_(universe),
                                   arr.item == item,
                                   arr.freq == freq,
                                   arr.fdate >= start,
                                   arr.fdate <= stop))
            return cash
        else:
            raise TypeError("index must be datetime slice")

import datetime
from sqlalchemy.sql import column, and_, or_
from estuarial.array.arraymanagementclient import ArrayManagementClient
from estuarial.util.dateparsing import check_date

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
            stop = inde.stop
            start, stop = check_date([start,stop])
            return start, stop
        else:
            raise TypeError("index must be datetime slice")

class _OHLCIndexer(_TRUniverseIndexer):

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = index.start
            stop = (index.stop)

            start,stop = check_date([start,stop])

            universe = self.obj.data.seccode.tolist()
            arr = self.obj.aclient['/DATASTREAM/ohlc.yaml']
            ohlc = arr.select(and_(arr.seccode.in_(universe)),
                               date_1 = start,
                               date_2 = stop,
                               )
            return ohlc
        else:
            raise TypeError("index must be datetime slice")

class _CASHIndexer(_TRUniverseIndexer):

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = index.start
            stop = (index.stop)

            start,stop = check_date([start,stop])

            universe = self.obj.data.seccode.tolist()
            item = 2001 # cash
            freq = 'Q'  # Quarterly Maybe use step for this?
            ws_query_loc = '/FUNDAMENTALS/WORLDSCOPE/worldscope_fundamentals.yaml'
            arr = self.obj.aclient[ws_query_loc]

            cash = arr.select(and_(arr.seccode.in_(universe),
                                   arr.item == item,
                                   arr.freq == freq
                                  ),
                               date_1 = start,
                               date_2 = stop
                             )
            return cash
        else:
            raise TypeError("index must be datetime slice")

class _NIIndexer(_TRUniverseIndexer):

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = index.start
            stop = (index.stop)

            start,stop = check_date([start,stop])
            universe = self.obj.data.seccode.tolist()
            item = 1751 # net income
            freq = 'Q'  # Quarterly Maybe use step for this?
            ni_query_loc = '/FUNDAMENTALS/WORLDSCOPE/worldscope_fundamentals.yaml'
            arr = self.obj.aclient[ni_query_loc]
            cash = arr.select(and_(arr.seccode.in_(universe),
                                   arr.item == item,
                                   arr.freq == freq,),
                               date_1 = start,
                               date_2 = stop,
                             )
            return cash
        else:
            raise TypeError("index must be datetime slice")

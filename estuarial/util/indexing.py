import datetime
from sqlalchemy.sql import column, and_, or_
from estuarial.array.arraymanagementclient import ArrayManagementClient
from estuarial.util.dateparsing import check_date
from estuarial.util.decorators import target_getitem


# the supported metrics
def get_metrics_list():
    return [('cash', _FundamentalIndexer,1751),
            ('ni', _FundamentalIndexer, 2001),
            ('ohlc', _OHLCIndexer, None),
            ]

class _TRUniverseIndexer(ArrayManagementClient):
    def __init__(self,obj,name, item):
        self.obj = obj
        self.name = name
        self.item = item


    def _slicer(self, slice_args):
        start = slice_args.start
        stop = slice_args.stop

        start_period,end_period = check_date([start,stop])

        return (start_period, end_period)




@target_getitem('_fundamentals', api_mapper='_slicer')
class _FundamentalIndexer(_TRUniverseIndexer):

    def _fundamentals(self, start_period, end_period):
        item = self.item

        universe = self.obj.data.seccode.tolist()
        freq = 'Q'  # Quarterly Maybe use step for this?
        ws_query_loc = '/FUNDAMENTALS/WORLDSCOPE/worldscope_fundamentals.yaml'
        arr = self.obj.aclient[ws_query_loc]

        data = arr.select(and_(arr.seccode.in_(universe),
                               arr.item == item,
                               arr.freq == freq
                              ),
                           date_1 = start_period,
                           date_2 = end_period
                         )
        return data

@target_getitem('_ohlc', api_mapper='_slicer')
class _OHLCIndexer(_TRUniverseIndexer):

    def _ohlc(self, start_period, end_period):

        universe = self.obj.data.seccode.tolist()
        arr = self.obj.aclient['/DATASTREAM/ohlc.yaml']
        ohlc = arr.select(and_(arr.seccode.in_(universe)),
                           date_1 = start_period,
                           date_2 = end_period,
                           )
        print(ohlc)
        return ohlc


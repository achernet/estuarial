import datetime
from sqlalchemy.sql import column, and_, or_
from estuarial.array.arraymanagementclient import ArrayManagementClient
from estuarial.util.dateparsing import check_date
from estuarial.util.decorators import target_getitem


# the supported metrics
def get_metrics_list():
    return [('cash', _FundamentalIndexer,1751),
            ('ni', _FundamentalIndexer, 2001),]

# dow.cash['2012-12-01':'2014-01-22']

@target_getitem('_fundamentals', api_mapper='_slicer')
class _FundamentalIndexer(ArrayManagementClient):
    def __init__(self,obj,name, item):
        self.obj = obj
        self.name = name
        self.item = item
        print(obj,name,item)


    def _fundamentals(self, start_period, end_period):
        item = self.item
        print(item)

        universe = self.obj.data.seccode.tolist()
        freq = 'Q'  # Quarterly Maybe use step for this?
        ws_query_loc = '/FUNDAMENTALS/WORLDSCOPE/worldscope_fundamentals.yaml'
        arr = self.obj.aclient[ws_query_loc]

        print(item)
        data = arr.select(and_(arr.seccode.in_(universe),
                               arr.item == item,
                               arr.freq == freq
                              ),
                           date_1 = start_period,
                           date_2 = end_period
                         )
        return data

    def _slicer(self, slice_args):
        start = slice_args.start
        stop = slice_args.stop

        start_period,end_period = check_date([start,stop])

        return (start_period, end_period)




# class _TRUniverseIndexer(ArrayManagementClient):
#
#     def __init__(self, obj, name):
#         self.obj = obj
#         self.name = name
#      def __getitem__(self, index):
#         if isinstance(index, slice):
#             start = index.start
#             stop = (index.stop)
#
#             start,stop = check_date([start,stop])
#
#             universe = self.obj.data.seccode.tolist()
#             arr = self.obj.aclient['/DATASTREAM/ohlc.yaml']
#             ohlc = arr.select(and_(arr.seccode.in_(universe)),
#                                date_1 = start,
#                                date_2 = stop,
#                                )
#             return ohlc
#         else:
#             raise TypeError("index must be datetime slice")
#
#
# class _OHLCIndexer(_TRUniverseIndexer):
#
#
#
# class _CASHIndexer(_TRUniverseIndexer):
#
#     def __getitem__(self, index):
#         if isinstance(index, slice):
#             start = index.start
#             stop = (index.stop)
#
#             start,stop = check_date([start,stop])
#
#             universe = self.obj.data.seccode.tolist()
#             item = 2001 # cash
#             freq = 'Q'  # Quarterly Maybe use step for this?
#             ws_query_loc = '/FUNDAMENTALS/WORLDSCOPE/worldscope_fundamentals.yaml'
#             arr = self.obj.aclient[ws_query_loc]
#
#             cash = arr.select(and_(arr.seccode.in_(universe),
#                                    arr.item == item,
#                                    arr.freq == freq
#                                   ),
#                                date_1 = start,
#                                date_2 = stop
#                              )
#             return cash
#         else:
#             raise TypeError("index must be datetime slice")
#
# class _NIIndexer(_TRUniverseIndexer):
#
#     def __getitem__(self, index):
#         if isinstance(index, slice):
#             start = index.start
#             stop = (index.stop)
#
#             start,stop = check_date([start,stop])
#             universe = self.obj.data.seccode.tolist()
#             item = 1751 # net income
#             freq = 'Q'  # Quarterly Maybe use step for this?
#             ni_query_loc = '/FUNDAMENTALS/WORLDSCOPE/worldscope_fundamentals.yaml'
#             arr = self.obj.aclient[ni_query_loc]
#             cash = arr.select(and_(arr.seccode.in_(universe),
#                                    arr.item == item,
#                                    arr.freq == freq,),
#                                date_1 = start,
#                                date_2 = stop,
#                              )
#             return cash
#         else:
#             raise TypeError("index must be datetime slice")

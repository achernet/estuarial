from __future__ import print_function, division, absolute_import

import os
import datetime as dt
from dateutil import parser
from os.path import join as pjoin
from sqlalchemy.sql import column, and_, or_
from estuarial.util.config.config import Config
from estuarial.util.munging import worldscope_align
from estuarial.util.dateparsing import parsedate
from estuarial.array.arraymanagementclient import ArrayManagementClient

class TRQAD(ArrayManagementClient):
    '''
    Functional style interface into TR's DB.  Most functions take 3 arguments:

    - Universe (list of entities)
    - Metrics (list of measurements)
    - Date Range

    '''

    def __init__(self, path=None):
        super(TRQAD, self).__init__()

    def ibes_detail_actuals(self, universe, measures, dt_list, freq='Q'):

        if isinstance(dt_list[0],dt.datetime):
            pass
        elif isinstance(dt_list[0],string):
            dt1 = parser.parse(dt_list[0])
            dt2 = parser.parse(dt_list[1])
            dt_list = (dt1,dt2)
        else:
            raise TypeError("dt_list must be valid datetime string YEAR-MN-DY "
                            "or datetime object")

        ibes_data = self.aclient['/IBES/ibd_actuals'].select(
            code=universe,
            measureCode=measures,
            freq=freq,
            fdate=[dt_list[0], dt_list[1]])

        return ibes_data

    def worldscope(self, universe, metrics,dt_list, freq='Q', align=False):
        """
        Query the WorldScope DB for metrics defined by the user
        with a given universe.  Metrics are fundamentals commonly
        found in balance sheets for equities data.

        :type universe: list
        :param universe: list of securities

        :type metrics: list
        :param metrics: list of metrics to pull from DB: (EPS, CASH, NI, etc.)

        :type dt_list: list/tuple
        :param dt_list: Beginning and end market dates for query

        :type freq: string
        :param freq: Frequency

        :type align: bool
        :param align: date align ddate

        :rtype: `pandas.DataFrame`
        :return: DataFrame of Securities with a TimeSeries of OHLC


        """

        start,stop = parsedate(dt_list)

        arr = self.aclient['/WORLDSCOPE/worldscope_metrics_date_select.yaml']
        ws_data = arr.select(
            and_(arr.seccode.in_(universe),
                 arr.item.in_(metrics),
                 arr.freq==freq),
            date_1=start,
            date_2=stop)

        if align:
            ws_data = worldscope_align(ws_data)
        return ws_data


    def datastream(self,universe,dt_list):
        """
        Query the Datastream DB for Open, High, Low, Close
        with a given universe (convenience function)

        :type universe: list
        :param universe: list of securities

        :type dt_list: list/tuple
        :param dt_list: Beginning and end market dates for query

        :rtype: `pandas.DataFrame`
        :return: DataFrame of Securities with a TimeSeries of OHLC

        """

        arr = self.aclient['/DataStream/datastream_basic.yaml']
        start,stop = parsedate(dt_list)

        df = arr.select(and_(arr.seccode.in_(universe),
                             arr.marketdate >= start,
                             arr.marketdate <= stop))
        return df



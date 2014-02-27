from __future__ import print_function, division, absolute_import


from feldman.config import Config

from sqlalchemy.sql import column, and_, or_
import datetime as dt
from os.path import join as pjoin
import os
import datetime as dt
from dateutil import parser
from feldman.arraymanagementclient import ArrayManagementClient



class TRQAD(ArrayManagementClient):
    '''
    Functional style interface into TR's DB.  Most functions take 3 arguments:

    - Universe (list of entities)
    - Metrics (list of measurements)
    - Date Range

    '''

    def __init__(self, path=None):
        super(TRQAD, self).__init__()


    def ibes_detail_actuals(self,universe,measures,dt_list,freq='Q'):

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
            fdate=[dt_list[0], dt_list[1]]
            )
        return ibes_data


    def worldscope(self,universe, metrics,dt_list,freq='Q'):
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

        :rtype: `pandas.DataFrame`
        :return: DataFrame of Securities with a TimeSeries of OHLC

        """

        ws_data = self.aclient['/WORLDSCOPE/wsndata.bsqlspec'].select(
                    seccode=universe,
                    item=metrics,
                    freq=freq,
                    fdate=[dt_list[0], dt_list[1]]
                    )
        return ws_data

    def datastream(self,universe,metrics, dt_list):
        """

        :param: metrics: open, high, low, close,
                vwap, totalreturn, volume, bid,
                ask, mosttrdprc, consolvol

        :type universe: list
        :param universe: list of securities

        :type dt_list: list/tuple
        :param dt_list: Beginning and end market dates for query

        :rtype: `pandas.DataFrame`
        :return: DataFrame of Securities with a TimeSeries of OHLC

        fd.metric.

        """


    def ds_ohlc(self,universe,dt_list):
        """
        Convenience method

        Query the Datastream DB for Open, High, Low, Close
        with a given universe (convenience function)

        :type universe: list
        :param universe: list of securities

        :type dt_list: list/tuple
        :param dt_list: Beginning and end market dates for query

        :rtype: `pandas.DataFrame`
        :return: DataFrame of Securities with a TimeSeries of OHLC

        """

        ds_data = self.aclient['/DataStream/ohlcview.sqlspec'].select(
                    seccode=universe,
                    marketdate=[dt_list[0],
                                dt_list[1]]
                    )

        return ds_data


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

        arr = self.aclient['/DataStream/datastream_basic.fsql']
        start, stop = dt_list
        df = arr.select(and_(arr.seccode.in_(universe),arr.marketdate >= start, \
                                        arr.marketdate <= stop))

        return df



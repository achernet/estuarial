from __future__ import print_function, division, absolute_import

import os
import sys
import datetime as dt
from dateutil import parser
from sqlalchemy.sql import column, and_, or_
from estuarial.util.config.config import Config
from estuarial.util.munging import worldscope_align
from estuarial.util.dateparsing import parsedate
from estuarial.array.arraymanagementclient import ArrayManagementClient
import posixpath

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

    def fundamentals(self, universe, metrics, dt_list, DB, freq='Q', align=False):
        """
        Query A Fundmentals DB for metrics defined by the user
        with a given universe.  Metrics are fundamentals commonly
        found in balance sheets for equities data.

        :type universe: list
        :param universe: list of securities

        :type metrics: list
        :param metrics: list of metrics to pull from DB: (EPS, CASH, NI, etc.)

        :type dt_list: list/tuple
        :param dt_list: Beginning and end market dates for query

        :type DB: string
        :param DB: Name of the fundamentals database -- Worldscope, RKD, etc

        :type freq: string
        :param freq: Frequency

        :type align: bool
        :param align: date align ddate

        :rtype: `pandas.DataFrame`
        :return: DataFrame of Securities with a TimeSeries of OHLC


        """
        db_dict = {"WORLDSCOPE":"worldscope_fundamentals.yaml",
                     "RKD":"rkd_fundamentals.yaml"
                    }


        DB = DB.upper()

        valid_dbs = db_dict.keys()

        if not DB in valid_dbs:
            dbs = ' '.join(valid_dbs)
            raise KeyError("Not a valid Database please use an approved DB: {}".format(dbs))

        if DB=='WORLDSCOPE':
            start, stop = parsedate(dt_list)
            df_file = db_dict[DB]
            url = posixpath.join('/FUNDAMENTALS',DB,df_file)
            arr = self.aclient[url]

            data = arr.select(
                and_(arr.seccode.in_(universe),
                     arr.item.in_(metrics),
                     arr.freq==freq),
                date_1=start,
                date_2=stop)

            if align:
                data = worldscope_align(data)

        if DB=='RKD':
            start, stop = parsedate(dt_list)
            df_file = db_dict[DB]
            url = posixpath.join('/FUNDAMENTALS',DB,df_file)
            arr = self.aclient[url]

            data = arr.select(
                and_(arr.code.in_(universe),
                     arr.coa.in_(metrics),
                     ),
                sourcedate_1=start,
                sourcedate_2=stop)
        return data


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

        arr = self.aclient['/DATASTREAM/datastream_basic.yaml']
        start,stop = parsedate(dt_list)

        df = arr.select(and_(arr.seccode.in_(universe),
                             arr.marketdate >= start,
                             arr.marketdate <= stop))
        return df



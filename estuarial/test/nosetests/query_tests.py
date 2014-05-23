from nose.tools import assert_dict_equal

import datetime as dt
from estuarial.query.trqad import TRQAD
from estuarial.query.raw_query import RAW_QUERY
import pandas as pd
import numpy as np
import os
import shutil
from estuarial.drilldown.metadata import TRMETA
from estuarial.browse.metrics_manager import MetricsManager
from estuarial.browse.universe_builder import UniverseBuilder

qad = TRQAD()

def setup_module():
    pass

def teardown_module():
    estuarial_path = os.path.join(os.path.expanduser('~'),'.estuarial')
    cache_path = os.path.join(estuarial_path,'.cache/')
    shutil.rmtree(cache_path)


def test_fundamentals():

    qad = TRQAD()
    IBM = 36799
    AAPL = 6027
    MSFT = 46692
    universe = [IBM,AAPL,MSFT]

    NI = 1751   # Net Income
    CASH = 2001 # Cash
    TL = 3351   # Total Liabilities

    dt_list = [dt.datetime(2000,1,1), dt.datetime(2014,1,1)]
    metrics_list = [NI, CASH, TL]
    df = qad.fundamentals(universe,metrics_list,dt_list,DB="WORLDSCOPE")
    df_sort = df.sort(['date','item'])

    locFirst = \
        {'date': pd.Timestamp('2000-06-30 00:00:00', tz=None),
         'ddate': pd.NaT,
         'freq': 'Q',
         'item': 1751,
         'seccode': 46692,
         'seq': 1,
         'value_': 2184000000.0,
         'year_': 2000}

    assert_dict_equal(locFirst,df_sort.iloc[0].to_dict())

    locLast = \
        {'date': pd.Timestamp('2013-12-31 00:00:00', tz=None),
         'ddate': pd.Timestamp('2013-09-30 00:00:00', tz=None),
         'freq': 'Q',
         'item': 3351,
         'seccode': 36799,
         'seq': 3,
         'value_': 94155000000.0,
         'year_': 2013}

    assert_dict_equal(locLast,df_sort.iloc[-1].to_dict())

    df = qad.fundamentals(universe,metrics_list,dt_list,DB="WORLDSCOPE",
                          align=True)

    df_sort = df.sort(['date','item'])

    locFirst = \
        {'date': pd.Timestamp('2000-06-30 00:00:00', tz=None),
         'ddate': pd.Timestamp('2000-03-30 00:00:00', tz=None),
         'freq': 'Q',
         'item': 1751,
         'seccode': 46692,
         'seq': 1,
         'value_': 2184000000.0,
         'year_': 2000}



    assert_dict_equal(locFirst,df_sort.iloc[0].to_dict())

    locLast = \
        {'date': pd.Timestamp('2013-12-31 00:00:00', tz=None),
         'ddate': pd.Timestamp('2013-09-30 00:00:00', tz=None),
         'freq': 'Q',
         'item': 3351,
         'seccode': 36799,
         'seq': 3,
         'value_': 94155000000.0,
         'year_': 2013}

    assert_dict_equal(locLast,df_sort.iloc[-1].to_dict())


def test_datastream():
    qad = TRQAD()
    IBM = 36799
    AAPL = 6027
    MSFT = 46692
    universe = [IBM,AAPL,MSFT]

    dt_list = (dt.datetime(2014,2,12), dt.datetime(2014,2,13))
    df = qad.datastream(universe, dt_list)
    df_sort = df.sort('marketdate')
    locFirst = \
        {'Ask': 535.90992000000006,
         'Bid': 535.85987,
         'Close_': 535.91993000000002,
         'ConsolVol': np.nan,
         'CumAdjFactor': 1,
         'ISOCurrCode': 'USD',
         'MostTrdPrc': np.nan,
         'MostTrdVol': np.nan,
         'Open_': 536.94996000000003,
         'VWAP': 536.51806999999997,
         'Volume': 11018149.0,
         'high': 539.55981999999995,
         'low': 533.24000000000001,
         'marketdate': pd.Timestamp('2014-02-12 00:00:00', tz=None),
         'seccode': 6027}
    assert_dict_equal(locFirst,df_sort.iloc[0].to_dict())

    locLast = \
        {'Ask': 37.609985999999999,
         'Bid': 37.599991000000003,
         'Close_': 37.609985999999999,
         'ConsolVol': np.nan,
         'CumAdjFactor': 1,
         'ISOCurrCode': 'USD',
         'MostTrdPrc': np.nan,
         'MostTrdVol': np.nan,
         'Open_': 37.329987000000003,
         'VWAP': 37.684387999999998,
         'Volume': 37647770.0,
         'high': 37.859985999999999,
         'low': 37.329987000000003,
         'marketdate': pd.Timestamp('2014-02-13 00:00:00', tz=None),
         'seccode': 46692}

    assert_dict_equal(locLast,df_sort.iloc[-1].to_dict())

def test_raw_query():
    rq = RAW_QUERY()

    #no access to CRSP
    df = rq.raw_query("select top 10 * from dbo.CrsPrcM")
    assert df.empty

    sql = '''
          select * from idxinfo where code in (select distinct idxcode
          from idxspcmp)
          '''

    df = rq.raw_query(sql)
    data = df[df['Code']==203].values
    sp500 = np.array([['SPX_IDX', 'SPX', 'S&P 500 INDEX', 203, 1]],
                     dtype=object)

    np.testing.assert_array_equal(data,sp500)




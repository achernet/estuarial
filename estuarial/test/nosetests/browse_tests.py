from nose.tools import assert_dict_equal
import pandas as pd
import numpy as np
import os
import shutil
import datetime as dt


from estuarial.browse.metrics_manager import MetricsManager
from estuarial.browse.universe_builder import UniverseBuilder
from estuarial.browse.market_index import MarketIndex
from pandas.util.testing import assert_frame_equal



def setup_module():
    pass

def teardown_module():
    estuarial_path = os.path.join(os.path.expanduser('~'),'.estuarial')
    cache_path = os.path.join(estuarial_path,'.cache/')
    shutil.rmtree(cache_path)


def test_metrics_manager():
    m = MarketIndex()

    data = m.constituents("S&P 500", '2012-12-31', '2012-12-31')
    data =  m["S&P 500", '2012-12-31']

    path = os.path.join('estuarial', 'test', 'nosetests',
                        'cached_data','cache_spx_universe.yaml.hdf5')

    cache_data = pd.HDFStore(path)
    df = cache_data['spx_universe.yaml']
    df_spx = df[df.ITICKER=='SPX_IDX']

    assert_frame_equal(df_spx, data)

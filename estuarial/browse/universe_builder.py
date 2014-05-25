from __future__ import print_function, division, absolute_import

from sqlalchemy.sql import and_
from estuarial.browse.universe import Universe
from estuarial.array.arraymanagementclient import ArrayManagementClient
from estuarial.util.munging import lower_columns

class UniverseBuilder(ArrayManagementClient):
    """
    universe builder and pre-defined universes
    These funcs should belong in the catalogue?
    check
    """

    def __init__(self):
        super(UniverseBuilder, self).__init__()

    @classmethod
    def us(self):
        conn = ArrayManagementClient()
        arr = conn.aclient['/DATASTREAM/equity_master.yaml']
        df = arr.select(and_(arr.ctrytradedin=='US',"IsPrimExchQt='Y'"))
        query = arr.query
        df = lower_columns(df)
        return Universe(df,query)

    @classmethod
    def can(self):
        conn = ArrayManagementClient()
        arr = conn.aclient['/DATASTREAM/equity_master.yaml']
        df = arr.select(and_(arr.ctrytradedin=='CA',
			     arr.statuscode=='A'))
        query = arr.query
        df = lower_columns(df)
        return Universe(df,query)

    @classmethod
    def world(self):
        conn = ArrayManagementClient()
        arr = conn.aclient['/DATASTREAM/equity_master.yaml']
        df = arr.select(arr.statuscode=='A')
        query = arr.query
        df = lower_columns(df)
        return Universe(df,query)

    @classmethod
    def djx_idx(self, dt):
        """
        :param dt: DateTime
        :return: Dow Jones Universe on a given date
        """
        conn = ArrayManagementClient()
        arr = conn.aclient['/UNIVERSE_SQL/dowjones_universe.yaml']
        df = arr.select(and_(arr.iticker=='DJX_IDX',arr.date_==dt))
        query = arr.query
        df = lower_columns(df)
        return Universe(df,query)

    @classmethod
    def spx_idx(self,dt):
        """
        :param dt: DateTime
        :return: SP500 Universe on a given date
        """
        conn = ArrayManagementClient()
        arr = conn.aclient['/UNIVERSE_SQL/spx_universe.yaml']
        df = arr.select(and_(arr.iticker=='SPX_IDX',arr.date_==dt))
        query = arr.query
        df = lower_columns(df)
        return Universe(df,query)
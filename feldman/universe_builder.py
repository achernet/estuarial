from __future__ import print_function, division, absolute_import


from feldman.config import Config
from arraymanagement.client import ArrayClient
from sqlalchemy.sql import column, and_, or_
import datetime as dt
from os.path import join as pjoin
import os

from feldman.arraymanagementclient import ArrayManagementClient
from feldman.universe import Universe

def lower_columns(df):
        """
        lower all column names
        """

        cols = [col.lower() for col in df.columns]
        df.columns = cols
        return df


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
        arr = conn.aclient['/UNIVERSE_SQL/country_universe.fsql']
        df = arr.select(and_(arr.ctrytradedin=='US',arr.statuscode=='A',arr.typecode=='EQ'))
        query = arr.query
        df = lower_columns(df)

        return Universe(df,query)


    @classmethod
    def can(self):
        conn = ArrayManagementClient()
        arr = conn.aclient['/UNIVERSE_SQL/country_universe.fsql']
        df = arr.select(and_(arr.ctrytradedin=='CA',arr.statuscode=='A',arr.typecode=='EQ'))
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
        arr = conn.aclient['/UNIVERSE_SQL/dowjones_universe.fsql']

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
        arr = conn.aclient['/UNIVERSE_SQL/spx_universe.fsql']

        df = arr.select(and_(arr.iticker=='SPX_IDX',arr.date_==dt))
        query = arr.query
        df = lower_columns(df)

        return Universe(df,query)




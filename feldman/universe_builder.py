from __future__ import print_function, division, absolute_import


from feldman.config import Config
from arraymanagement.client import ArrayClient
from sqlalchemy.sql import column, and_, or_
import datetime as dt
from os.path import join as pjoin
import os

from feldman.arraymanagementclient import ArrayManagementClient


class universe_builder(ArrayManagementClient):
    """
    universe builder and pre-defined universes
    These funcs should belong in the catalogue?
    check
    """

    def __init__(self):
        super(universe_builder, self).__init__()

    @classmethod
    def us(self):
        conn = ArrayManagementClient()
        arr = conn.aclient['UNIVERSE_SQL/country_universe.fsql']
        df = arr.select(and_(arr.CtryTradedIn=='US',arr.StatusCode=='A',arr.TypeCode=='EQ'))
        return df

    @classmethod
    def can(self):
        conn = ArrayManagementClient()
        arr = conn.aclient['UNIVERSE_SQL/country_universe.fsql']
        df = arr.select(and_(arr.CtryTradedIn=='CA',arr.StatusCode=='A',arr.TypeCode=='EQ'))
        return df


us = fd.universe.us()
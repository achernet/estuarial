from __future__ import print_function, division, absolute_import

from sqlalchemy.sql import column, and_, or_

from feldman.arraymanagementclient import ArrayManagementClient


class Universe(ArrayManagementClient):
    """
    universe object
    """

    def __init__(self,DataFrame):
        super(Universe, self).__init__()
        self.data = DataFrame

    def __repr__(self):
        return ("TR Universe")

    def __str__(self):
        return ("TR Universe")

    @property
    def EPS(self):
        '''NET INCOME USED TO CALCULATE BASIC EARNINGS PER SHARE
        problems, no arguments for freq, datetime
        '''

        universe = self.data.seccode.tolist()
        chunksize = 2000
        chunks  = [ universe[start:start+chunksize] for start in range(0, len(universe), chunksize)]
        item=1705
        freq='Q'

        arr  = self.aclient['worldscope_metrics/wsndata.fsql']
        eps = [arr.select(and_(arr.seccode.in_(chunk),arr.item==item,arr.freq==freq)) for chunk in chunks]
        return eps

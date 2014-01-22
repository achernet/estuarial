from __future__ import print_function, division, absolute_import

from sqlalchemy.sql import column, and_, or_
import datetime as dt
from feldman.arraymanagementclient import ArrayManagementClient
import feldman.indexing as indexing

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
    def NI(self):
        '''NET INCOME USED TO CALCULATE BASIC EARNINGS PER SHARE
        problems, no arguments for freq, datetime
        '''

        universe = self.data.seccode.tolist()
        chunksize = 2000
        chunks  = [universe[start:start+chunksize] for start in range(0, len(universe), chunksize)]

        # 5201 	EARNINGS PER SHARE
        item = 1751
        freq='Q'

        arr  = self.aclient['/WORLDSCOPE/worldscope_metrics.fsql']

        ni = [arr.select(and_(arr.seccode.in_(chunk),arr.item==item,arr.freq==freq)) for chunk in chunks]
        return ni

    @classmethod
    def _create_metrics(cls, name, metric_class):
        """
        fancy method of instantiating object

        """

        if getattr(cls, name, None) is None:
            underscore_name = '_%s' % name
            setattr(cls, underscore_name, None)

            def _metric_loader(self):
                i = getattr(self, underscore_name)
                if i is None:
                    i = metric_class(self, name)
                    setattr(self, underscore_name, i)
                return i

            setattr(cls, name, property(_metric_loader))


for _name, _metric_class in indexing.get_metrics_list():
    Universe._create_metrics(_name, _metric_class)

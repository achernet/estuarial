from __future__ import print_function, division, absolute_import

import datetime as dt
import estuarial.util.indexing as indexing
from sqlalchemy.sql import column, and_, or_
from estuarial.array.arraymanagementclient import ArrayManagementClient

class Universe(ArrayManagementClient):
    """
    universe object
    """

    def __init__(self, DataFrame, Query=None):
        super(Universe, self).__init__()
        self.data = DataFrame
        self._sql = Query

    def __repr__(self):
        return ("TR Universe")

    def __str__(self):
        return ("TR Universe")

    @classmethod
    def _create_metrics(cls, name, metric_class, item):
        """
        fancy method of instantiating object
        """

        if getattr(cls, name, None) is None:
            underscore_name = '_%s' % name
            setattr(cls, underscore_name, None)

            def _metric_loader(self):
                i = getattr(self, underscore_name)
                if i is None:
                    i = metric_class(self, name, item)
                    setattr(self, underscore_name, i)
                return i

            setattr(cls, name, property(_metric_loader))

for _name, _metric_class, item in indexing.get_metrics_list():
    Universe._create_metrics(_name, _metric_class, item)


if __name__ == "__main__":
    from estuarial.browse.universe_builder import UniverseBuilder
    spx = UniverseBuilder.spx_idx('2013-12-04')
    df =  spx.data
    spx.data = df[df.name.str.contains("Machine")]
    # spx.ohlc['2009-01-01':'2014-01-01']
    print(spx.cash['2013-01-01':'2014-01-01'].head())
    print(spx.ni['2012-01-01':'2014-01-01'].head())



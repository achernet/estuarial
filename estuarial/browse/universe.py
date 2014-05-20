from __future__ import print_function, division, absolute_import

import datetime as dt
import estuarial.util.indexing as indexing
from sqlalchemy.sql import column, and_, or_
from sqlalchemy.sql.expression import literal_column
from estuarial.array.arraymanagementclient import ArrayManagementClient


class Universe(ArrayManagementClient):
    """
    universe object
    """

    def __init__(self, DataFrame, Query = None):
        super(Universe, self).__init__()
        self.data = DataFrame
        self._sql = Query

    def __repr__(self):
        return ("TR Universe")

    def __str__(self):
        return ("TR Universe")

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

    def to_vencodetype(self, ventype):
        """
        :param ventype: QADirect ventype of supplied vencodes
        :return: df mapping vencode to infocode
        """
        codes_out = []
        code_count = self.data.infocode.count()
        # Sql Server appears to have a 64kb query size limitation.
        # This translates to roughly 10K US seccodes we can pass in, a bit less for global.
        # (hack hack hack)
        BATCH_SIZE = 7500
        num_batches = int(round(code_count / float(BATCH_SIZE))) + 1
        for i in range(0, num_batches):
            start = i * BATCH_SIZE
            end = start + BATCH_SIZE - 1
            if (start >= code_count):
                break
            if (end >= code_count):
                end = code_count - 1

            print("batch: " + str(i) + " start/end: " + str(start) + "/" + str(end))
            codes_in = [int(x) for x in self.data.infocode[start:end]]
            conn = ArrayManagementClient()
            arr = conn.aclient['/DATASTREAM/equity_map.yaml']
            infocode_filter = literal_column("infocode IN (select * from trqa.CSVToTable('%s', ','))" % ','.join(
                [str(x) for x in codes_in]))
            df = arr.select(and_(arr.ventype == ventype, infocode_filter))
            codes_out += [int(x) for x in df.vencode]
            print(len(codes_out))
        return codes_out



for _name, _metric_class in indexing.get_metrics_list():
    Universe._create_metrics(_name, _metric_class)

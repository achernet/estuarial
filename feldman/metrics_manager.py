from __future__ import print_function, division, absolute_import

from feldman.arraymanagementclient import ArrayManagementClient
import string

class WS(ArrayManagementClient):
    def __init__(self):
        super(WS, self).__init__()
        arr = self.aclient['/WORLDSCOPE/wsitems.sql']
        df = arr.select()

        for t_metric in df.values:

            name = t_metric[1].translate(None,string.punctuation).replace(' ','_')
            value = t_metric[0]
            setattr(self, name, value)


class MetricsManager(ArrayManagementClient):
    def __init__(self):
        super(MetricsManager, self).__init__()
        self.ws = WS()

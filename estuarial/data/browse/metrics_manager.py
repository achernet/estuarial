from __future__ import print_function, division, absolute_import

import string
from collections import Counter
from difflib import get_close_matches
from estuarial.array.arraymanagementclient import ArrayManagementClient

class WS(ArrayManagementClient):

    def __init__(self):
        super(WS, self).__init__()
        arr = self.aclient['/WORLDSCOPE/wsitems.sql']
        df = arr.select()
        self.word_list = None
        for t_metric in df.values:
            name = t_metric[1].translate(None,
                                         string.punctuation).replace(' ','_')
            value = t_metric[0]
            setattr(self, name, value)

    def _word_list(self):
        arr = self.aclient['/WORLDSCOPE/wsitems.sql']
        df = arr.select()
        word_list = df.Name.values.tolist()

        #lots of cleanup :)
        words = ' '.join(word_list)
        words = words.translate(None,string.punctuation+string.digits)
        words = words.replace('OF','')

        c_words = Counter(words.split())
        common = c_words.most_common(30)
        common = [com[0] for com in common]

        return common

    def find_metrics(self,name=None):
        arr = self.aclient['/WORLDSCOPE/wsitems.sql']
        df = arr.select()
        if not self.word_list:
            self.word_list = self._word_list()

        name = str(name)
        found = df[df.Name.str.contains(name,case=False)]

        if found.empty:
            close = get_close_matches(name, self.word_list)
            if close:
                message = "Error: Could not find '%s' in Worldscope Items"
                message += '\n\nDid you mean one of these?\n'
                message = message % name
                for s in close:
                    message += '    %s' % s

                #handle return gracefully
                print(message)
                return None

        return found

class DS(object):

    columns = ['Open_',
               'High',
               'Low',
               'Close_',
               'Volume',
               'Bid',
               'Ask',
               'VWAP',
               'MostTrdPrc',
               'ConsolVol',
               'MostTrdVol']

    def __init__(self):
        for val in self.columns:
            name = val.translate(None,
                                 string.punctuation).replace('_','').upper()
            setattr(self, name, val)

class MetricsManager(ArrayManagementClient):
    def __init__(self):
        super(MetricsManager, self).__init__()
        self.ws = WS()
        self.ds = DS()

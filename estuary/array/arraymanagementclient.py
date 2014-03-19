from __future__ import print_function, division, absolute_import

import os
from os.path import join as pjoin
from arraymanagement.client import ArrayClient
from estuary.util.config.config import expanduser, UserConfigPath

if not 'ODBCINI' in os.environ:
    os.environ['ODBCINI'] = UserConfigPath

class ArrayManagementClient(object):
    """
    Hangle ArrayManagement Connection
    """

    def __init__(self):
        FeldmanDir = pjoin(expanduser('~'), '.estuary')
        self.basedir = pjoin(os.path.dirname(__file__), 
                             '..',
                             'data', 
                             'catalog', 
                             'SQL_DATA')
        self.aclient = ArrayClient(basepath=self.basedir, 
                                   localdatapath=FeldmanDir)

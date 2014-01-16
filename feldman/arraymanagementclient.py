from __future__ import print_function, division, absolute_import


from arraymanagement.client import ArrayClient
from os.path import join as pjoin
import os

class ArrayManagementClient(object):
    """
    Hangle ArrayManagement Connection
    """

    def __init__(self):
        self.basedir = pjoin(os.path.dirname(__file__),'SQL_DATA')
        self.aclient = ArrayClient(self.basedir)

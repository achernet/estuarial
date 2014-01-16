import pandas
import pyodbc
import os
import re
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, event
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.engine import Engine
import json

class SQLContentSet():
    """ Class for aggregating tablespecs and mapping into a logical set """
    
    """these properties should all be abstracted to interfaces - DM"""
    @property
    def content_sets(self):
        return self._content_sets
    
    @property
    def managed_views(self):
        return self._managed_views
    
    @property
    def managed_procs(self):
        return self._managed_procs
    
    @property
    def entities(self):
        return self._entities
    
    @property
    def metrics(self):
        return self._metrics
    
    def __init__(self, meta):
        self._meta = meta
        
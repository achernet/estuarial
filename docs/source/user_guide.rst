.. _userguide:

User Guide
==========

Estuarial comes preloaded with a catalog of SQL queries designed to help users explore and fetch the data from
TRQAD.  The queries are written with a bit of markup (YAML) and are exposed through python -- offering several
conveniences over simple wrapped raw SQL.  As Estuarial develops the catalog will also develop and become more
comprehensive overtime.  The time series data we can currently can fetch is limited to fundamental data (Worldscope and
RKD) and end of day data (Datastream).  We also have built-out a number of mechanisms to help navigate metadata
vital for filtering time series and understand the financial world.

There are three styles/methods of using estuarial: *query*, *drilldown*, and *browse*.  These three styles map to
the three modes of analysis: production, exploration, debugging.

Production
----------

The Query object aims to represent the most generalized form of queries.  Most functions take 3 arguments: a list of
entities, a list of metrics, and a date range::

    >>> from estuarial.query.trqad import TRQAD

    >>> qad = TRQAD()
    >>> qad.fundamentals(universe,metrics_list,dt_list,DB="WORLDSCOPE")

Date is automatically cached in HDF5 and returned back as a Pandas DataFrame.  For production queries, users often
come to estuarial with a list of known entities, dates, etc.  To query for end of day data::

    >>> df = qad.datastream(universe, dt_list)


import datetime as dt
from estuarial.query.trqad import TRQAD
from estuarial.drilldown.metadata import TRMETA
from estuarial.browse.metrics_manager import MetricsManager
from estuarial.browse.universe_builder import UniverseBuilder


.. include:: includes/databases/datastream.rst
.. include:: includes/databases/datastream.rst
.. include:: includes/databases/datastream.rst
.. include:: includes/databases/datastream.rst


Catalogue
    Custom Queries
        Yaml Syntax
universe
fundamentals
datastream
metadata
styles
    query
    drilldown
    browse
        Market Indices

.. _userguide:

==========
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

Exploration
-----------

The beginning of any analytic work flow starts with exploring the data.  Exploration conveys a sense of immediacy and
limited scope.  For Estuarial, this means building common starting points, attaching convenience methods whenever
possible, and metadata browsing.

Entity Creation
===============

    >>> from estuarial.browse.market_index import MarketIndex
    >>> m = m = MarketIndex()
    >>> m.constituents("Russell 1000", '2012-12-28')
    >>> m["S&P 500",'2014-01-01':'2014-02-01']

.. autoclass:: estuarial.browse.market_index.MarketIndex
   :members:
   :undoc-members:

*Note Universe Builder is experimental*.  Entities limited to SP500, Dow Jones, currently trade US stocks, and
currently traded CAN stocks::

    >>> from estuarial.browse.universe_builder import UniverseBuilder
    >>> spx = UniverseBuilder.spx_idx("2013-12-04")
    >>> spx = UniverseBuilder.spx_idx(dt.datetime(2013, 12, 4))

``TR Universe`` object stores dataframe in ``data`` attribute.  Attached are also several methods for querying data
with the universe as a set of entities::

    >>> spx.ohlc['2009-01-01':'2014-01-01'] #return Open, High, Low, Close between dt1:dt2
    >>> spx.cash['2009-01-01':'2014-01-01'] #return CASH fundamental from Worlscope between dt1:dt2


.. autoclass:: estuarial.browse.universe_builder.UniverseBuilder
   :members:
   :undoc-members:

Metadata
========

    >>> from estuarial.browse.metrics_manager import MetricsManager
    >>> metrics = MetricsManager()
    >>> metrics.ws.<tab><tab>
    >>> metrics.rkd.<tab><tab>

leverage ipython
    >>> metrics.rkd.*Restaurants*?
    >>> metrics.ws.*DEBT*?

Production
----------

The Query object aims to represent the most generalized form of queries.  Most functions take 3 arguments: a list of
entities, a list of metrics, and a date range::

    >>> from estuarial.query.trqad import TRQAD

    >>> qad = TRQAD()
    >>> qad.fundamentals(universe,metrics_list,dt_list,DB="WORLDSCOPE")

Data is automatically cached in HDF5 and returned back as a Pandas DataFrame.  For production queries, users often
come to Estuarial with a list of known entities, dates, etc.  To query for end of day data::

    >>> df = qad.datastream(universe, dt_list)

And to query fundamentals data::

    >>> df = qad.fundamentals(universe,metrics_list,dt_list,DB="WORLDSCOPE")

.. autoclass:: estuarial.query.trqad.TRQAD
   :members:
   :undoc-members:
   :exclude-members: ibes_detail_actuals


..
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

.. _userguide:

==========
User Guide
==========
Estuarial is an open-source financial data analysis platform developed for
use with ad-hoc data sets as well as pre-configured data sets supplied from
Thomson Reuters QAD. The goal of Estuarial is to solve many of the data access,
array computing, caching, and software engineering roadblocks that currently
result in quantitative analysts spending more time preparing the data than 
performing research. 

There are three major modes of use for Estuarial: raw querying, browsing pre-
configured data sources, and drilling down to get specific information about a
particular query or piece of data (usually for debugging). These are organized
into the top-level sub-packages of the project, :code:`query`, :code:`browse`, 
and :code:`drilldown`. 

- :code:`query`: Contains facilities to perform raw queries contained in Python
  strings. Future development will include methods for mirroring parts
  of the available data infrastructure directly in Python.

- :code:`browse`: Contains convenience functions that perform commonly-needed 
  data access patterns against pre-configured data sources. New data sources
  can be added to the configuration so that :code:`browse` tools can be used
  even with custom data sets.

- :code:`drilldown`: Contains metadata access code for introspecting available 
  items, learning how entities are mapped between data locations, and debugging
  the pieces of some data access pipeline when it gives unexpected results.


In addition to the three main sub-packages, a few other sub-packages exist:

- :code:`data`: Location for software to handle connections to the data and to
  interpret special markup (Yaml documents) that extend a database access
  pattern into Python.

- :code:`util`: Location for odds and ends code needed to be centrally 
  maintained and tested together, but which is used frequently in the rest of 
  the library.

- :code:`array`: Contains adapters which allow the library to connect to 
  different array computing backend tools.

- :code:`test`: Location of the projects tests.

Partial support exists for convenience-layer queries and metadata for the 
following vendors: DataStream, WorldScope, RKD, and IDC -- with increasing and
extended support for more vendors and data sets being added continuously.


Browse
-----------

The beginning of many analytic work flows is browsing the data.  Exploration 
conveys a sense of immediacy and limited scope.  For Estuarial, this means 
building common starting points, attaching convenience methods whenever 
possible, and metadata browsing.

Index Constituents
==================

One basic operation is retrieving a set of point-in-time constituents
belonging to a particular market index. The :code:`MarketIndex` class 
encapsulates this functionality as in the following examples::

    >>> from estuarial.browse.market_index import MarketIndex
    >>> m = MarketIndex()
    >>> m.constituents("Russell 1000", '2014-01-01', '2014-02-01')

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 21294 entries, 0 to 21293
    Data columns (total 10 columns):
    INAME                  21294  non-null values
    ITICKER                21294  non-null values
    TICKER                 21294  non-null values
    CUSIP                  21294  non-null values
    NAME                   21294  non-null values
    DATE_                  21294  non-null values
    CLOSE_                 21294  non-null values
    SHARES                 21292  non-null values
    SECCODE                21294  non-null values
    RELATIVE_MARKET_CAP    21292  non-null values
    dtypes: datetime64[ns](1), float64(3), int64(1), object(5)


    >>> m["S&P 500", '2012-12-28']
    
    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 500 entries, 0 to 499
    Data columns (total 10 columns):
    INAME                  500  non-null values
    ITICKER                500  non-null values
    TICKER                 500  non-null values
    CUSIP                  500  non-null values
    NAME                   500  non-null values
    DATE_                  500  non-null values
    CLOSE_                 500  non-null values
    SHARES                 500  non-null values
    SECCODE                500  non-null values
    RELATIVE_MARKET_CAP    500  non-null values
    dtypes: datetime64[ns](1), float64(3), int64(1), object(5) 

Currently there is support for the S&P BMI country and regional indices, the
S&P 100, 500, and 1000, the Russell 1000, 2000, and 3000, and Dow Jones.

.. autoclass:: estuarial.browse.market_index.MarketIndex
   :undoc-members:


Universe Constituents
=====================

Aside from pre-existing indices, analysts often want to look at baskets of 
financial instruments grouped by geographic, industrial, or other common
categorical information. 

The :code:`Universe` exists to encapsulate the point-in-time membership for 
these categories. The returned :code:`Universe` object stores a 
:code:`pandas.DataFrame` in the attribute :code:`data` attribute, with entity
information about each returned security. Below is an example for the current
list of all U.S. stocks.::


    >>> from estuarial.browse.universe_builder import UniverseBuilder
    >>> us_constituents = UniverseBuilder.us()
    >>> us_constituents.data

    Int64Index: 28052 entries, 0 to 28051
    Data columns (total 11 columns):
    infocode        28052  non-null values
    isocurrcode     28052  non-null values
    isprimexchqt    28052  non-null values
    exchintcode     28052  non-null values
    ctrytradedin    28052  non-null values
    statuscode      28052  non-null values
    typecode        28052  non-null values
    seccode         28052  non-null values
    ctryofissuer    28052  non-null values
    ventype         28052  non-null values
    vencode         28052  non-null values

:code:`Universe` can also be used to retrieve market index information, similar 
to :code:`MarketIndex` but with optional ability to align and retrieve other
metrics (described in the next section).::

    >>> spx = UniverseBuilder.spx_idx("2013-12-04")
    >>> spx = UniverseBuilder.spx_idx(dt.datetime(2013, 12, 4))
    >>> spx.data

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 500 entries, 0 to 499
    Data columns (total 10 columns):
    iname                  500  non-null values
    iticker                500  non-null values
    ticker                 500  non-null values
    cusip                  500  non-null values
    name                   500  non-null values
    date_                  500  non-null values
    close_                 500  non-null values
    shares                 500  non-null values
    seccode                500  non-null values
    relative_market_cap    500  non-null values
    dtypes: datetime64[ns](1), float64(3), int64(1), object(5)


Retrieving Metrics Aligned to Universe Constituents
===================================================

From the example above, the :code:`Universe` object has several methods for 
querying data aligned to the universe as a set of entities::

    >>> spx.ohlc['2009-01-01':'2014-01-01'] #return Open, High, Low, Close
    >>> spx.cash['2009-01-01':'2014-01-01'] #return CASH fundamental from WorldScope
    >>> spx.ni['2009-01-01':'2014-01-01']   #return Net Income from WordlScope

The implementation of attributes such as :code:`ohlc` and :code:`cash` is 
easily extendable, both as part of new release updates that work with the pre-
configured data sets and also derived from user-defined queries. See the 
section on extended the tool with custom queries for more information.

*Note* :code:`UniverseBuilder` *is experimental*.  Entities limited to S&P 500, 
Dow Jones, currently traded US or Canadian stocks. Expect some functionality 
between :code:`MarketIndex` and :code:`UniverseBuilder` to be refactored.

.. autoclass:: estuarial.browse.universe_builder.UniverseBuilder
   :members:


Drilldown
---------

One important time-cost to analysts is inspecting data schema or architecture
information. The :code:`drilldown` sub-package allows for quick, 
*within-Python* inspection of schema information, such as what item names or 
codes are available from different vendors.::

    >>> from estuarial.browse.metrics_manager import MetricsManager
    >>> metrics = MetricsManager()
    >>> metrics.ws.<tab><tab>
    >>> metrics.rkd.<tab><tab>

An immediate advantage is seen by leveraging IPython tab completion and pattern
matching to view available items::

    >>> metrics.rkd.*Restaurants*?
    >>> metrics.ws.*DEBT*?

Query
-----

The :code:`query` sub-package aims to represent the most generalized form of 
queries reflected in Python. The API restricts functions to take three arguments: 
a list of entities, a list of metrics, and a date range::

    >>> from estuarial.query.trqad import TRQAD
    >>> qad = TRQAD()
    >>> qad.fundamentals(universe, metrics_list, dt_list, DB="WORLDSCOPE")

Data is automatically cached using advanced features of the Python PyTables 
library and the HDF5 data format. Data is returned back as a 
:code:`pandas.DataFrame`.  To query for end of day data from DataStream::

    >>> df = qad.datastream(universe, dt_list)

and to query fundamentals data from WorldScope::

    >>> df = qad.fundamentals(universe, metrics_list, dt_list, DB="WORLDSCOPE")

.. autoclass:: estuarial.query.trqad.TRQAD
   :undoc-members:
   :exclude-members: ibes_detail_actuals


How Estuarial Interacts with SQL Queries
----------------------------------------

Estuarial is designed to work with pre-configured SQL query documents as well as
those created and added to the tool by the end users. This process involves 
storing a query in a specially marked-up format as part of a Yaml document, 
with some extra annotations regarding documentation and the names of components 
of the returned data that should be contrainable for controlling the scope of
the query.


Singleton Yaml Documents
========================

For working with a single SQL query, Estuarial uses a markup format known as Yaml
to contain a name for the query, some documentation, the query string itself, and
annotations about which fields in the query should serve as keyword arguments
that can be used from Python to generate :code:`WHERE` statements for restricting
the result set of the query.

We have see the :code:`ohlc` functionality in the sections above; here is the Yaml
document that contains the SQL statements needed for this query.::

    SQL:
        ohlc:
            doc: Some OHLC documentation.

            conditionals:
                - seccode
                - marketdate
    
            query: >
                select m.seccode
                  , marketdate
                  , Open_
                  , high
                  , low
                  , Close_
                  , q.ISOCurrCode
                  , case priceunit
                               when 'E+02' then 100
                         else 1
                        end as CumAdjFactor
                from Ds2PrimQtPrc q
                join secmapx m
                    on m.vencode = q.infocode
                    and m.ventype = 33 and rank = 1
                join ds2Adj a
                    on a.infocode = q.infocode
                    and q.marketdate between adjdate and isnull(endadjdate, '2079-06-06')
                    and AdjType = 2
                join ds2exchqtinfo e
                    on e.infocode = q.infocode
                   and e.startdate < q.marketdate
                   and q.exchintcode = e.exchintcode
    

The :code:`doc` section provides a string describing the query. This string 
can serve as the documentation string within the resulting Python code as well 
so it is important to provide descriptive documentation.

The :code:`conditionals` section declares columns that will result in the data
fetched by the query -- these columns will act as keyword arguments in Python to
allow for on-the-fly :code:`WHERE` clause constraints placed on them.

Finally, the :code:`query` section is a multi-line string containing the actual
SQL query itself. This is where user-supplied SQL code can be pasted to 
automatically generate Python structures that will perform the query.

Composite Yaml Documents
========================

Much like the singleton Yaml document described above, composite Yaml documents
contain :code:`doc`, :code:`conditionals`, and :code:`query` sections that work
the same way. The difference is that at the top-level of the document, a name
is given instead of the keyword "SQL". This name will be the name of a 
constructed Python class. 

The other major difference is that the file can contain more than one SQL query.
Each of the provided queries will become a different member function belonging
to the constructed class. You can thinking of the constructed class as a 
convenience object meant to hold a bundle of releated SQL queries (in their 
Python function form).

See the section below on using :code:`QueryHandler` for an example of a composite
Yaml document and guidelines for how to use them.

Introduction to :code:`QueryHandler`
====================================

Within the :code:`data` sub-package exists the class :code:`QueryHandler` for
ingesting composite Yaml documents as described above and translating them into
Python classes with queries exposed as if they were user-defined functions.

.. autoclass:: estuarial.data.query_handler.QueryHandler
    :undoc-members:


Using :code:`QueryHandler`
==========================

Consider the following sample composite query file which is saved in
"/test/test_example.yaml" relative to :code:`QueryHandler._FILE_DIR`.::

    
    AccountingData:                                      
        inventory:                                       
            doc: This is a query for inventory.          
            conditionals:                                
                account_id: A customer's account number. 
                shipping_date: The shipping date.        
            query: >                                     
                SELECT                                   
                      a.account_id as account_id         
                    , b.shipping_id as shipping_id       
                    , a.customer_name                    
                    , b.shipping_date                    
                    , b.order_volume                     
                    , b.total_sales                      
                FROM account_table a                     
                JOIN shipping_table b                    
                    ON a.account_id = b.shipping_id      
                                                         
        payroll:                                         
            doc: This is a payroll query.                
            conditionals:                                
                branch_id: A branch id number            
                city: A city name                        
            query: >                                     
                SELECT                                   
                      a.branch_id                        
                    , b.city                             
                    , a.total_payroll as branch_payroll  
                    , b.total_payroll as city_payroll    
                FROM branch_table a                      
                JOIN branch_location_table b             
                    ON a.branch_id = b.branch_id         
    

The :code:`QueryHandler.create_type_from_yaml` function will create a new 
Python class, :code:`AccountingData` that has two functions:::

    # These return pandas.DataFrame representations of the data returned
    # from the query.
    AccountingData.inventory
    AccountingData.payroll

and will have attributes for the known conditional arguments and the query
strings as well:::

    # The file location of a generated yaml file that stores just the 
    # "inventory" section from the composite yaml file.
    AccountingData.__inventory_file

    # A string of the raw query for the inventory function.
    AccountingData.__inventory_query
    
    # A list of strings naming the different conditional arguments that 
    # were listed for the inventory function.
    AccountingData.__inventory_kwargs

    # These are repeated for any other functions as well:
    AccountingData.__payroll_file
    AccountingData.__payroll_query
    AccountingData.__payroll_kwargs

Let's look at the :code:`inventory` query. Because the file declares 
:code:`accounting_id` as a conditional name, that name will be interpreted as
something that should be available as an argument for the :code:`inventory`
function, such as :code:`inventory(accounting_id=10)`. 

Under the hood, this will generate a SQL :code:`WHERE` condition (as in, 
:code:`WHERE accounting_id = 10`) that will get applied to the base results of
whatever plain query was given for the inventory entry in the yaml file.

In this manner, the function inventory acts like a specifier for :code:`WHERE`
conditions for the query it was given, such that only the items listed as
conditionals can appear in the :code:`WHERE` statements.

So if we wanted to see the result of the inventory query where 
:code:`account_id` is 10 and :code:`shipping_date` is '2012-12-31', we could 
say:::

    qh = QueryHandler()
    AccountingData = qh.create_type_from_yaml('test/test_example.yaml')
    ad = AccountingData()
    data = ad.inventory(accounting_id=10, shipping_date='2012-12-31')

But what about more options for the arguments? 

This is handled with special keyword arguments that extend the given
conditional names to include other operations, like :code:`BETWEEN` or 
:code:`>=` or :code:`IS NOT`. These are shown below:::

    # No use of any WHERE conditions
    ad.inventory()

    # WHERE account_id = 10
    ad.inventory(account_id=10)

    # WHERE account_id != 10
    ad.inventory(account_id_not_equal=10)

    # WHERE account_id > 10
    ad.inventory(account_id_greater_than=10)

    # WHERE account_id >= 10
    ad.inventory(account_id_greater_than_or_equal=10)

    # WHERE account_id < 10
    ad.inventory(account_id_less_than=10)

    # WHERE account_id <= 10
    ad.inventory(account_id_less_than_or_equal=10)

    # WHERE account_id BETWEEN 10 AND 20
    ad.inventory(account_id_between=(10, 20))

    # WHERE account_id IN (10, 11, 12)
    ad.inventory(account_id_in=(10, 11, 12))

    # WHERE account_id NOT IN (10, 11, 12)
    ad.inventory(account_id_not_in=(10, 11, 12))

    # WHERE account_id IS NULL
    ad.inventory(account_id_is=None)

    # WHERE account_id IS NOT NULL
    ad.inventory(account_id_is_not=None)
    ad.inventory(account_id_not_equal=None)

To demonstrate string operations, we'll use the :code:`city` variable from the
:code:`payroll` function:::

    # WHERE city LIKE '%York%'
    ad.payroll(city_like=" '%York%' ")

    # WHERE city NOT LIKE '%York%'
    ad.payroll(city_not_like=" '%York%' ")

    # WHERE city ILIKE '%york%'
    ad.payroll(city_ilike=" '%york%' ")

    # WHERE city NOT ILIKE '%york%'
    ad.payroll(city_not_ilike=" '%york%' ")

And some string conveniences are defined for matching the start or end of
a string, and also checking if a string contains something. The appropriate
SQL equivalent is given, assuming :code:`<pattern>` represents the text to be 
matched.::

    # WHERE city LIKE '%<pattern>%'
    ad.payroll(city_contains="<pattern>")

    # WHERE city LIKE '<pattern>%'
    ad.payroll(city_startswith="<pattern>")        

    # WHERE city LIKE '%<pattern>'
    ad.payroll(city_endswith="<pattern>")     

The "doc" keyword that appeared in the yaml file will create the function's
documentation, along with the keyword arguments:::

    help(ad.inventory)
    print ad.inventory.__doc__
    
These will display:::

    This is a query for inventory.

    Params
    ------
    account_id: A customer's account number.
    shipping_date: The shipping date.

By mimicking this example composite Yaml document and placing it in the
the location for custom SQL queries, a user can automatically generate a Python
class which embodies as functions whatever queries are desired , with keyword
arguments to control the :code:`WHERE` statements.


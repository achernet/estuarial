.. _quickstart:

##########
Quickstart
##########

Downloading/Installing
----------------------

There are several ways to install Feldman:

If you are using the `Anaconda Python distribution <http://continuum.io/anaconda>`_:
::

    $ conda install feldman
    $ pip install feldman


To download from source, clone the `Feldman git repo <https://github.com/ContinuumIO/feldman>`_,
then run:
::

    $ python setup.py install



Using Feldman
-------------

Once installed you can now easily query the TR database in two styles:

- OO/Attribute oriented is great for exploration and developing routines::

    dow = fd.UniverseBuilder.djx_idx('2014-01-28')
    dow.cash['2012-12-01':'2014-01-22']

- A more functional style is also available for those with pre-built universes or for production routines::

    universe = data ## list of seccodes
    NI = 1751   # Net Income
    CASH = 2001 # Cash
    TL = 3351   # Total Liabilities

    dt_list = (dt.datetime(2000,1,1), dt.datetime(2014,1,1))
    metrics = [NI,CASH,TL]
    tr.worldscope(universe,metrics,dt_list)


Example IPython Notebooks
-------------------------



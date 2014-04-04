.. _universe:

##########
Universe
##########

Pre-defined universes are a great starting point for any financial analytic. We've created a number of convenience
accessors to help get you started.::

    spx = fd.UniverseBuilder.spx_idx('2013-12-04')
    dow = fd.UniverseBuilder.djx_idx('2014-01-28')
    us = fd.UniverseBuilder.us()
    can = fd.UniverseBuilder.can()



Estuarial Universe objects are built for easy exploration::

    dow.cash[dt1:dt2]
    dow.ohlc['2013-12-01':'2014-01-22']


Source
------
.. autoclass:: estuarial.UniverseBuilder
   :members:
   :undoc-members:

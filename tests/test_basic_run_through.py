import datetime as dt
import feldman as fd

tr = fd.TRQAD()
spx = fd.UniverseBuilder.spx_idx('2013-12-04')
spx = fd.UniverseBuilder.spx_idx(dt.datetime(2013, 12, 4))


universe = spx.data.seccode.tolist()[:20]
NI = 1751   # Net Income
CASH = 2001 # Cash
TL = 3351   # Total Liabilities
STD = 3051  # Short Term Debt
LTD = 3251  # Long Term Debt
TD = 3255   # Total Debt
TA = 2999   # Total Assets

dt_list = (dt.datetime(2000,1,1), dt.datetime(2014,1,1))
metrics = [NI,CASH,TL]
tr.worldscope(universe,metrics,dt_list)

spx = fd.UniverseBuilder.spx_idx('2013-12-04')
df =  spx.data
spx.data = df[df.name.str.contains("Machine")]
spx.ohlc['2009-01-01':'2014-01-01']
spx.cash['2009-01-01':'2014-01-01']

us = fd.UniverseBuilder.us()
can = fd.UniverseBuilder.can()

dow = fd.UniverseBuilder.djx_idx('2014-01-28')
dow.cash['2012-12-01':'2014-01-22']
dow.ohlc['2013-12-01':'2014-01-22']
dow.ni['2013-12-01':'2014-01-22']
dow.XXXXXX
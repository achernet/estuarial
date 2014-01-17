import datetime as dt
import feldman as fd

tr = fd.TRQAD()
spx = fd.UniverseBuilder.spx_idx('2013-12-04')
spx = fd.UniverseBuilder.spx_idx(dt.datetime(2013, 12, 4))


universe = spx.data.SECCODE.tolist()[:20]
NI = 1751   # Net Income
CASH = 2001 # Cash
TL = 3351   # Total Liabilities
STD = 3051  # Short Term Debt
LTD = 3251  # Long Term Debt
TD = 3255   # Total Debt
TA = 2999   # Total Assets

dt_list = (dt.datetime(2000,1,1), dt.datetime(2014,1,1))
metrics = [NI,CASH,TL]
tr.ws_meas(universe,metrics,dt_list)

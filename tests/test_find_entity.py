import feldman
import datetime as dt

tr = feldman.TRQAD()


ents = tr.find_entity()

IBM_HOPEFULLY = ents.select(ents.seccode==36799)

tr.find_entity(entity='AAPL')

spx = tr.spx_idx('2013-12-04')
spx = tr.spx_idx(dt.datetime(2013, 12, 4))


universe = spx.SECCODE.tolist()[:20]
NI = 1751   # Net Income
CASH = 2001 # Cash
TL = 3351   # Total Liabilities
STD = 3051  # Short Term Debt
LTD = 3251  # Long Term Debt
TD = 3255   # Total Debt
TA = 2999   # Total Assets

dt_list = (dt.datetime(2000,1,1), dt.datetime(2014,1,1))
metrics = [NI,CASH,TL]
tr.get_ws_data(universe,metrics,dt_list)


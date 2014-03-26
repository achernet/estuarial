import datetime as dt
from estuarial.query.trqad import TRQAD
from estuarial.browse.universe_builder import UniverseBuilder
 
qad = TRQAD()

spx = UniverseBuilder.spx_idx(dt.datetime(2013, 12, 4))
universe = spx.data.seccode.tolist()[:20]

IBM = 36799
AAPL = 6027
MSFT = 46692

NI = 1751   # Net Income
CASH = 2001 # Cash
TL = 3351   # Total Liabilities
STD = 3051  # Short Term Debt
LTD = 3251  # Long Term Debt
TD = 3255   # Total Debt
TA = 2999   # Total Assets

dt_list = [dt.datetime(2000,1,1), dt.datetime(2014,1,1)]
metrics_list = [NI, CASH, TL]
df = qad.fundamentals(universe,metrics_list,dt_list,DB="WORLDSCOPE")
print df.head()


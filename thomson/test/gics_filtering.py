import datetime as dt
from thomson.data.browse.trqad import TRQAD
from thomson.data.drilldown.metadata import TRMETA
from thomson.data.browse.universe_builder import UniverseBuilder

# Parameters used for testing.
IBM = 36799
NI = 1751   # Net Income
CASH = 2001 # Cash
TL = 3351   # Total Liabilities
STD = 3051  # Short Term Debt
LTD = 3251  # Long Term Debt
TD = 3255   # Total Debt
TA = 2999   # Total Assets
ws_dt_list = (dt.datetime(2000,1,1), dt.datetime(2014,1,1))
ws_metrics = [NI,CASH,TL]
spx_date = '2013-12-04'

# Thomson data fetchers.
qad = TRQAD()
meta = TRMETA()

# Testing worldscope data.
some_ws_data = qad.worldscope(universe, metrics, dt_list)

# Testing SPX universe creation.
spx = UniverseBuilder.spx_idx('2013-12-04')

# Testing GICS meta data.
gics_df = meta.gics
gics_df.rename(columns={'SECCODE':'seccode'}, inplace=True)

a = df.merge(gics_df,on=['seccode'])
print a[a.SECTOR.str.contains('Information')],head().to_string()


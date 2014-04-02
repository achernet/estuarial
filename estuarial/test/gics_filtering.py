import datetime as dt
from estuarial.query.trqad import TRQAD
from estuarial.drilldown.metadata import TRMETA
from estuarial.browse.universe_builder import UniverseBuilder

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


# Testing SPX universe creation.
spx = UniverseBuilder.spx_idx('2014-02-10')
df = spx.data

# Testing GICS meta data.
print meta.gicidx
gics_df = meta.gics('2014-01-31')
print gics_df.head()

gics_df.rename(columns={'SECCODE':'seccode'}, inplace=True)

a = df.merge(gics_df,on=['seccode'])
print a[a.SECTOR.str.contains('Information')].head().to_string()


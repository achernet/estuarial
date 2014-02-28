import datetime as dt
import feldman as fd


IBM = 36799
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

trmeta = fd.TRMETA()
gics_df = gics_df = trmeta.gics
gics_df.rename(columns={'SECCODE':'seccode'},inplace=True)

a = df.merge(gics_df,on=['seccode'])
a[a.SECTOR.str.contains('Information')]

new_universe = fd.filter_gics(universe,gic_code)
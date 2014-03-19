from estuary.data.browse.trqad import TRQAD
from sqlalchemy.sql import column, and_, or_
from estuary.data.browse.universe_builder import UniverseBuilder

tr = TRQAD()
c = tr.aclient

spx = UniverseBuilder.spx_idx('2013-12-04')
universe = spx.data.seccode.tolist()[:20]

[[2099, 5689, 3122, 3788, 6088],
 [5930, 5678, 28262, 15770, 11295],
 [14316, 14343, 18740, 24305, 25392],
 [26099, 27913, 32530, 36947, 37133]]

chunksize = 2000
chunks = [universe[start:start+chunksize] 
          for start in range(0, len(universe), chunksize)]

item = 1705
freq = 'Q'

arr = c['/WORLDSCOPE/worldscope_metrics.fsql']
df = [arr.select(and_(arr.seccode.in_(chunk), 
                      arr.item==item, 
                      arr.freq==freq))
      for chunk in chunks]

us = UniverseBuilder.us()
universe = us.data.seccode.tolist()
chunksize = 2000
chunks = [universe[start:start+chunksize] 
          for start in range(0, len(universe), chunksize)]

us = UniverseBuilder.us()
ca = UniverseBuilder.ca()
spx = UniverseBuilder.spx_idx('2013-12-04')

us.EPS
us.ohlc('2012-01-01')

df = tr.ws_meas([seccodes],[NI, CASH, EPS],(dt_begin,dt_end))
df = tr.ws_meas([seccodes],[NI, CASH, EPS])[dt_begin:dt_end]

# Possibly moved to meta
tr.find_entity('AAPL')
tr.gic

def filter_df(df, **kwargs):
  temp_df = df
  for colname, values in kwargs.items():
  #don't force users to wrap single item lists that are strings

  if type(values) == type(""):
  values = [values]
  f_df1 = temp_df[colname]
  f_df2 = f_df1.isin(values)
  temp_df = temp_df[f_df2]
  return temp_df

filter_df(T_pg_b60_df, 
          ProductGroup=['Energy', 
                        'Agriculture', 
                        'InterestRates', 
                        'Equities'])


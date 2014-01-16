import feldman as fd
from sqlalchemy.sql import column, and_, or_

tr = fd.TRQAD()
c = tr.aclient

spx = fd.UniverseBuilder.spx_idx('2013-12-04')
universe = spx.data.SECCODE.tolist()[:20]

[[2099, 5689, 3122, 3788, 6088],
 [5930, 5678, 28262, 15770, 11295],
 [14316, 14343, 18740, 24305, 25392],
 [26099, 27913, 32530, 36947, 37133]]

chunksize = 5
chunks = [ universe[start:start+chunksize] for start in range(0, len(universe), chunksize)]

item = 1705
freq = 'Q'

arr = c['WSNDATA/wsndata.fsql']
df = [arr.select(and_(arr.seccode.in_(chunk),arr.item==item,arr.freq==freq)) for chunk in chunks]

us = fd.UniverseBuilder.us()
universe = us.data.seccode.tolist()
chunksize = 2000
chunks = [ universe[start:start+chunksize] for start in range(0, len(universe), chunksize)]

import datetime as dt
from estuarial.query.trqad import TRQAD
from estuarial.drilldown.metadata import TRMETA
from estuarial.browse.metrics_manager import MetricsManager
from estuarial.browse.universe_builder import UniverseBuilder
 
qad = TRQAD()
meta = TRMETA()
metrics = MetricsManager()

spx = UniverseBuilder.spx_idx('2013-12-04')
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
qad.fundamentals(universe,metrics_list,dt_list,DB="WORLDSCOPE")

#reduce universe to IBM
df =  spx.data
spx.data = df[df.name.str.contains("Machine")]
spx.ohlc['2009-01-01':'2014-01-01']
spx.cash['2009-01-01':'2014-01-01']

meta.find_entity_name('BMW')
meta.find_entity_id(36799)
print meta.gicidx
gics = meta.gics(date='2014-03-31')
print gics
gics[gics.SECCODE==36799]

us = UniverseBuilder.us()
print us.data.head()
can = UniverseBuilder.can()

dow = UniverseBuilder.djx_idx('2014-01-28')
dow.cash['2012-12-01':'2014-01-22']
dow.ohlc['2013-12-01':'2014-01-22']
dow.ni['2013-12-01':'2014-01-22']

print metrics.ws.CASH
print metrics.ds.OPEN

dt_list = (dt.datetime(2014,2,12), dt.datetime(2014,2,13))
df = qad.datastream(dow.data.seccode.tolist(), dt_list)
print df.head()

from estuarial.query.raw_query import RAW_QUERY

rquery = RAW_QUERY()
sql = '''
select * from idxinfo where code in (select distinct idxcode from idxspcmp)
'''

print rquery.raw_query(sql)



from estuarial.drilldown.metadata import TRMETA


meta = TRMETA()
meta.to_rkdcode([36799])
import datetime as dt
from estuarial.browse.metrics_manager import MetricsManager
from estuarial.browse.universe_builder import UniverseBuilder
from estuarial.drilldown.metadata import TRMETA

metrics = MetricsManager()



assert metrics.rkd.Restaurants=='MRSB'
print metrics.rkd.find_metrics("Restaurants")


meta = TRMETA()

spx = UniverseBuilder.spx_idx('2013-12-04')
seccodes = spx.data.seccode.tolist()[:5]
print seccodes[:5]

rkd_verse = meta.to_rkdcode(seccodes)
print rkd_verse.head()


from estuarial.query.trqad import TRQAD
qad = TRQAD()
dt_list = [dt.datetime(2000,1,1), dt.datetime(2014,1,1)]

# Diluted EPS Excluding ExtraOrd Items
# Total Debt

metrics_list = ['SDBF','STLD']
universe = rkd_verse.seccode.tolist()

rkd_data = qad.fundamentals(universe=universe,metrics=metrics_list,dt_list=dt_list,DB="RKD")
print rkd_data.head()

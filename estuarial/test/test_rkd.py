import datetime as dt
from estuarial.browse.metrics_manager import MetricsManager
from estuarial.browse.universe_builder import UniverseBuilder
from estuarial.drilldown.metadata import TRMETA

metrics = MetricsManager()



assert metrics.rkd.Restaurants=='MRSB'
print metrics.rkd.find_metrics("Restaurants")


meta = TRMETA()

spx = UniverseBuilder.spx_idx('2013-12-04')
seccodes = spx.data.seccode

rkd_secs = meta.to_rkdcode(seccodes)





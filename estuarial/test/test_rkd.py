import datetime as dt
from estuarial.browse.metrics_manager import MetricsManager

metrics = MetricsManager()



assert metrics.rkd.Restaurants=='MRSB'
print metrics.rkd.find_metrics("Restaurants")

#print metrics.rkd.




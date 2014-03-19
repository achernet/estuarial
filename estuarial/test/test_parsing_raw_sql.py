import datetime as dt
from estuarial.data.drilldown.metadata import TRMETA

trmeta = TRMETA()
trmeta.to_fsql('tr_total_returns.sql',
               'tr_total_returns.fsql')

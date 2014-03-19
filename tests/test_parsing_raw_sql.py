import estuary
import datetime as dt

trmeta = estuary.TRMETA()


trmeta.to_fsql('tr_total_returns.sql','tr_total_returns.fsql')

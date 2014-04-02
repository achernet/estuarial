from estuarial.drilldown.metadata import TRMETA


meta = TRMETA()
print meta.to_rkdcode(seccodes=[36799])
print meta.to_rkdcode(tickers=['IBM'])
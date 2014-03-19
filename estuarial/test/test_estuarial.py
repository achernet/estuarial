from estuarial.data.browse import (universe, 
                                   metrics_manager,
                                   universe_builder)

print dir(universe)
print dir(metrics_manager)
print dir(universe_builder)

ub = universe_builder.UniverseBuilder
spx = ub.spx_idx('2013-12-04')
dow = ub.djx_idx('2013-12-04')

print dow.ohlc['2013-12-01':'2014-01-22'].to_string()




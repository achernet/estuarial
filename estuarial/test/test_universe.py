from estuarial.data.browse.universe_builder import UniverseBuilder

spx = UniverseBuilder.spx_idx('2013-12-04')
dow = UniverseBuilder.djx_idx('2013-12-04')
dow.ohlc['2013-12-01':'2014-01-22']




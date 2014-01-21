import feldman as fd

spx = fd.UniverseBuilder.spx_idx('2013-12-04')

spx.NI
spx.CASH
spx.EPS
spx.LTD
spx.BLAHABLAHB

spx.ohlc

spx.ohlc('')

fd.ws_meas[begin:end](codes,[NI,CASH,EPS],,freq='Q')



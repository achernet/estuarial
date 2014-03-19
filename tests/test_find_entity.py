import estuary as fd

trmeta = fd.TRMETA()

ents = trmeta.find_entity()

IBM_HOPEFULLY = ents.select(ents.seccode==36799)

trmeta.find_entity_name(entity='AAPL')
trmeta.find_entity_id(entity=36799)

trmeta.find_entity_name('BMW')
trmeta.find_entity_name('BMW',origin='non-us')

trmeta.find_entity_name('Bayerische')
trmeta.find_entity_name('Bayerische',origin='non-us')

bmw_name = tr.find_name('Bayerische')

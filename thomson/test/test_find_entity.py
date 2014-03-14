from thomson.data.drilldown.metadata import TRMETA 

meta = TRMETA()
#ents = meta.find_entity_id()
#IBM_HOPEFULLY = ents.select(ents.seccode==36799)

meta.find_entity_name(entity='AAPL')
meta.find_entity_id(entity=36799)

meta.find_entity_name('BMW')
meta.find_entity_name('BMW', origin='non-us')

meta.find_entity_name('Bayerische')
meta.find_entity_name('Bayerische', origin='non-us')

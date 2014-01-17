import feldman as fd
import datetime as dt

tr = fd.TRQAD()


ents = tr.find_entity()

IBM_HOPEFULLY = ents.select(ents.seccode==36799)

tr.find_entity(entity='AAPL')




import os, json,sys, ConfigParser
from SQLDataSource import SQLServerDataSource
import pyodbc
import code

os.chdir('..')

config = json.load(open('./data_sources/qadirect/qadirect.json'))

qad = SQLServerDataSource(config)


#code.interact(local=locals())

config = ConfigParser.ConfigParser()
config.readfp(open('./db_objects/Ds2PrimQtInfo2.view'))
config.sections()
#config.get('SQL', 'name')

for section in config.sections():
    qad.drop_and_create_view(section, config.get(section,'sql'))
##viewSpec = config.get('SQL', 'name'), config.get('SQL', 'sql')

#cursor = qad.conn.cursor()

#tr.create_codes_temp_table((1,2,3),cursor)


import code
code.interact(local=locals())



# print 'single security-single measurement'
# jnj =  tr.query('JNJ','ws.1751','Q')

# print jnj

# print 'single security-multiple measurements'
# # ibm = tr.query('IBM',1751,'Q']
# ibm = tr.query('IBM',['ws.1751','ws.2001','ws.3351'],'Q')

# print ibm
# print ibm.data.keys()

# print 'multiple securities-single measurments'
# ni_secs = tr.query(['IBM','APPL','GOOG'],'ws.1751','Q')

# print ni_secs
# print ni_secs.data.keys()

#re.sub(r'palantir\\.(\\w*)', r'palantir.\1_qadpy',"select * from palantir.test")
#
#creds = json.load(open('./config/trkeys.json'))
#
#creds = json.loads('''
#{
#    "Uid": "qas_test",
#    "Pwd": "qasqasqas",
#    "driver": "SQL Server Native Client 10.0",
#    "Server": "10.143.14.62",
#    "Port": "1433"
#}
#''')
#conn = pyodbc.connect('Driver={%s};Server={%s};Database=qai;Uid={%s};Pwd={%s}'%(creds['driver'],creds['server'],creds['Uid'],creds['Pwd']))
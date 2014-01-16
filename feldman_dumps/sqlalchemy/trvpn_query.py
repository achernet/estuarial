import sqlalchemy
import iopro 
from iopro import pyodbc
from sqlalchemy import Index, Table, Column, Integer, String, MetaData, ForeignKey, create_engine
from sqlalchemy import DateTime, SmallInteger, Float, VARCHAR
from sqlalchemy import DateTime as SmallDateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy import and_
import pandas as pd

'''
The patch is simple.  Create a file named:
~/anaconda/lib/python2.7/site-packages/iopro.pth
With the following content:
iopro
https://groups.google.com/a/continuum.io/forum/#!msg/anaconda/tI7tgQFLhFw/oQbyKH7y2v0J
'''

base = declarative_base()
creds = {
    "Uid": "qas_test",
    "Pwd": "qasqasqas",
    "driver": "/opt/microsoft/sqlncli/lib64/libsqlncli-11.0.so.1790.0",
    "server": "10.143.14.62,1433"
}


# db = create_engine('mssql+pyodbc://qas_test:qasqasqas@10.143.14.62:1433/qai', encoding='latin1', echo=True)

conn = iopro.pyodbc.connect('Driver={%s};Server={%s};Database=qai;Uid={%s};Pwd={%s}'%(creds['driver'],creds['server'],creds['Uid'],creds['Pwd']))


# db = create_engine('mssql+pyodbc://bzaitlen:ZuLUpmxs@107.21.201.126:2866/', encoding='latin1', echo=True)
def get_conn():
    conn = iopro.pyodbc.connect('Driver={%s};Server={%s};Database=qai;Uid={%s};Pwd={%s}'%(creds['driver'],creds['server'],creds['Uid'],creds['Pwd']))
    return conn

sql = '''
SELECT  I.NAME
    ,   S.TICKER
    ,   S.CUSIP
    ,   S.NAME
    ,   N.DATE_
    ,   D.CLOSE_
    ,   N.SHARES
    ,   M.SECCODE
    ,   D.CLOSE_ * N.SHARES AS RELATIVE_MARKET_CAP
FROM         DBO.IDXSPCMP N
    JOIN     DBO.IDXINFO I
        ON  I.CODE = N.IDXCODE
    JOIN     PRC.IDXSEC S
        ON  S.CODE = N.SECCODE
        AND S.VENDOR = 1 -- S&P
    JOIN     DBO.SECMAP M
        ON  M.SECCODE = S.PRCCODE
        AND M.VENTYPE = 14 -- IDC Pricing
        AND M.EXCHANGE = 1 -- US
    JOIN     PRC.PRCDLY D
        ON  D.CODE = M.VENCODE
        AND D.DATE_ =(  SELECT  MAX(DATE_)
                    FROM     PRC.PRCDLY
                    WHERE   CODE = D.CODE
                    AND DATE_ <= N.DATE_    )
WHERE       N.DATE_ = ?
    AND I.TICKER = ?
ORDER BY    RELATIVE_MARKET_CAP DESC
'''

cursor = conn.cursor()
data = cursor.execute(sql,'2013-12-04','SPX_IDX').fetchdictarray()
df = pd.DataFrame.from_dict(data)

sql = '''
select m.seccode, d.year_, d.seq, d.date_, d.value_, f.date_ from wsndata d
join secmapx m on m.ventype = 10 and m.vencode = d.code and rank = 1
left outer join wsfye f on f.code = d.code and f.year_ = d.year_
where m.seccode in (%s) and item = ? and freq = ?'''

secs = ', '.join('?' for sec in SPX.SECCODE.values)
sql = sql % secs


NI = '1751'
FREQ = 'Q'

ents = [int(sec) for sec in SPX.SECCODE.values]

params = ents+[NI,FREQ]

cursor.execute(sql,params)
data = cursor.fetchdictarray()
df = pd.DataFrame.from_dict(data)

#select IBM
df[df['seccode'] == int(IBM)].head(5)

Run function here to get SP500 

function that takes seccode 

establish blaze array around world scope and in aray format 

MAGICALLY GET SP500
df[(df.SECCODE == ?) & (df.METRIC == ?)]

#World Scope example
BLZ['SP500']['IBM']['A GIVEN METRIC']

df = f('SP500', 'IBM')
df[df.SECCODE=51207]

db = create_engine('mssql://', creator = get_conn, encoding='latin1', echo=True)
Session = sessionmaker(bind=db)
session=Session()

metadata = MetaData()

class WSNDATA(base):
    __tablename__ = 'wsndata'
    code = Column('Code', Integer, primary_key=True)
    item = Column('Item', Integer, primary_key=True)
    freq = Column('Freq', VARCHAR, primary_key=True)
    year_ = Column('Year_', SmallInteger, primary_key=True)
    seq_ = Column('Seq', Integer, primary_key=True)
    date_ = Column('Date_', SmallDateTime)
    value_ = Column('Value_', Float)

class SECMAPX(base):
    __tablename__ = 'secmapx'
    seccode = Column('SecCode', Integer, primary_key=True)
    ventype = Column('VenType', SmallInteger, primary_key=True)
    vencode = Column('VenCode', Integer) 
    rank = Column('Rank', SmallInteger, primary_key=True)
    exchange = Column('Exchange', SmallInteger)
    startdate = Column('StartDate', DateTime)
    enddate = Column('EndDate', DateTime)

    
class WSFYE(base):
    '''
    World Scope Fiscal Year end Dates
    Table returns fiscal year end dates for a given Worlscope entity ID
    '''

    __tablename__ = 'wsfye'
    # code = Column('Code', Integer, ForeignKey('wsndata.code'), primary_key=True)
    # year_ = Column('Year_', SmallInteger, ForeignKey('wsndata.year_'), primary_key=True)
    code = Column('Code', Integer, primary_key=True)
    year_ = Column('Year_', SmallInteger, primary_key=True)
    date_ = Column('Date_', SmallDateTime)


query = session.query(WSNDATA.year_, WSNDATA.seq_, WSNDATA.date_, WSNDATA.value_, WSFYE.date_, SECMAPX.seccode).\
        join(SECMAPX, and_(SECMAPX.ventype == 10, SECMAPX.vencode == WSNDATA.code, SECMAPX.rank == 1)).\
        outerjoin(WSFYE, and_(WSFYE.code == WSNDATA.code, WSFYE.year_ == WSNDATA.year_)).\
        filter(SECMAPX.seccode.in_([IBM,AAPL,GOOG]), WSNDATA.item == 1751, WSNDATA.freq == 'Q')


data_records = [rec.__dict__ for rec in query.all()]
df = pd.DataFrame.from_records(data_records)
df = df.drop(['_labels'],axis=1)

#select IBM
df[df['seccode'] == int(IBM)].head(5)

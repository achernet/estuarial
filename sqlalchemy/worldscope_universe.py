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

base = declarative_base()
creds = {
    "Uid": "bzaitlen",
    "Pwd": "ZuLUpmxs",
    "driver": "/usr/local/lib64/libsqlncli-11.0.so.1790.0",
    "server": "107.21.201.126,2866"
}
conn = iopro.pyodbc.connect('Driver={%s};Server={%s};Database=qai;Uid={%s};Pwd={%s}'%(creds['driver'],creds['server'],creds['Uid'],creds['Pwd']))


# db = create_engine('mssql+pyodbc://bzaitlen:ZuLUpmxs@107.21.201.126:2866/', encoding='latin1', echo=True)
def get_conn():
    conn = iopro.pyodbc.connect('Driver={%s};Server={%s};Database=qai;Uid={%s};Pwd={%s}'%(creds['driver'],creds['server'],creds['Uid'],creds['Pwd']))
    return conn

sql = '''
select m.seccode, d.year_, d.seq, d.date_, d.value_, f.date_ from wsndata d
join secmapx m on m.ventype = 10 and m.vencode = d.code and rank = 1
left outer join wsfye f on f.code = d.code and f.year_ = d.year_
where m.seccode in (?, ?, ?) and item = ? and freq = ?'''

NI = '1751'
FREQ = 'Q'

IBM = '36799'
GOOG = '30902'
AAPL = '6027'

params = [IBM,GOOG,AAPL,NI,FREQ]

cursor = get_conn().cursor()
cursor.execute(sql,params)
df = pd.DataFrame.from_dict(data)

#select IBM
df[df['seccode'] == IBM].head(5)



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
df[df['seccode'] == IBM].head(5)


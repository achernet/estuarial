import calendar
import numpy as np
from dateutil import parser
import pandas as pd

import requests
import zipfile
import StringIO

url = 'http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors.zip'
r = requests.get(url)
z = zipfile.ZipFile(StringIO.StringIO(r.content))
z.extractall()


def last_weekday(row):
    year, month = int(row[:4]),int(row[4:])
    day =  np.asarray(
        calendar.monthcalendar(year, month))[:,:5].max()
    date = '-'.join([str(year),str(month),str(day)])
    return parser.parse(date)


df = pd.read_csv('F-F_Research_Data_Factors.txt',
                    skiprows=3,delimiter='   ',
                    names=['date','Mkt-RF','SMB','HML','RFRF'],header=True,skipfooter=2)

index = np.where(df.date.str.contains('Annual Factors').values ==True)[0][0]

df = df.ix[:index].dropna()
df['Date'] = df['date'].apply(last_weekday)
df = df.drop(['date'],axis=1)
df.set_index(['Date'],inplace=True)
for col in df.columns:
    df[col] = df[col].astype('float64')

df.to_csv('fama.csv',cols=['Mkt-RF','SMB','HML','RFRF'],index=True)


import sqlite3
from pandas.io import sql as psql
conn = sqlite3.connect('fama.db')
psql.write_frame(df, name='FAMA', con=conn)
conn.close()


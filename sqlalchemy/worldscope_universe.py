import iopro 
from iopro import pyodbc
import pandas as pd
import numpy as np

creds = {
    "Uid": "qas_test",
    "Pwd": "qasqasqas",
    "driver": "/opt/microsoft/sqlncli/lib64/libsqlncli-11.0.so.1790.0",
    "server": "10.143.14.62,1433"
}


NI = 1751   # Net Income 
CASH = 2001 # Cash
TL = 3351   # Total Liabilities
STD = 3051  # Short Term Debt
LTD = 3251  # Long Term Debt
TD = 3255   # Total Debt
TA = 2999   # Total Assets


def get_conn():
    conn = iopro.pyodbc.connect('Driver={%s};Server={%s};Database=qai;Uid={%s};Pwd={%s}'%(creds['driver'],creds['server'],creds['Uid'],creds['Pwd']))
    return conn

def get_props_foreach_ticker(entities, metrics):

    #default frequency to QUARTERLY
    FREQ = 'Q'

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
    cursor = get_conn().cursor()
    data = cursor.execute(sql,'2013-12-04','SPX_IDX').fetchdictarray()
    df_q1 = pd.DataFrame.from_dict(data)

    #find proper seccodes
    seccodes = [df_q1[df_q1['TICKER'] == sec]['SECCODE'].values[0] for sec in entities]

    #cursor doesn't like numpy.int32 convert to int
    seccodes = [int(sec) for sec in seccodes]

    sql = '''
          select item, m.seccode, d.year_, d.seq, d.date_, d.value_, f.date_ from wsndata d
          join secmapx m on m.ventype = 10 and m.vencode = d.code and rank = 1
          left outer join wsfye f on f.code = d.code and f.year_ = d.year_
          where m.seccode in (%s) and item in (%s) and freq = ?
          '''
    
    secs = ', '.join('?' for sec in seccodes)
    mets = ', '.join('?' for m in metrics)
    sql = sql % (secs,mets)

    print sql

    params = seccodes+metrics+[FREQ]
    cursor.execute(sql,params)
    data = cursor.fetchdictarray()
    df_q2 = pd.DataFrame.from_dict(data)

    df_q2['ticker'] = df_q2['seccode']
    df_q2['ticker'] = df_q2['ticker'].astype('str')
    
    for code, tick in zip(seccodes, entities):
        df_q2['ticker'].replace(code,tick,inplace=True)
    
    return df_q2


df = get_props_foreach_ticker(['IBM','AAPL','MSFT'], [NI,CASH,TL,STD,TA])

print df.head(5)

#select IBM
print df[df['ticker'] == 'IBM'].head(5)

#select IBM and Net Income
print df[(df['ticker'] == 'IBM') & (df['item'] == NI)].head(5)













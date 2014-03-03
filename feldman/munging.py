from dateutil.relativedelta import relativedelta
import numpy as np

def worldscope_align(df):

    for count, row in df.iterrows():
        if row['ddate'] is np.nan and row['fdate'] is not np.nan:
            if row['seq'] == 4:
                row['ddate'] = row['fdate']
            elif row['seq'] == 3:
                row['ddate'] = row['fdate'] + relativedelta(months=-3)
            elif row['seq'] == 2:
                row['ddate'] = row['fdate'] + relativedelta(months=-6)
            elif row['seq'] == 1:
                row['ddate'] = row['fdate'] + relativedelta(months=-9)
            lastfy = row['fdate']
        elif row['ddate'] is np.nan and row['fdate'] is np.nan:
            row['ddate'] = lastfy + relativedelta(months=3*row['seq'])
        df.loc[count,'ddate'] = row['ddate']

    return df
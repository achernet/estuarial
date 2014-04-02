import numpy as np
from dateutil.relativedelta import relativedelta

# Helper function to align worldscope data wih possibly 
# different reporting dates.
def worldscope_align(df):
    for count, row in df.iterrows():
        if row['ddate'] is np.nan and row['fdate'] is not np.nan:
            assert row['seq'] in range(1, 5)
            sh_months = 4 - row['seq']
            row['ddate'] = row['fdate'] + relativedelta(months=-1*sh_months)
            last_fisc_yr = row['fdate']
        elif row['ddate'] is np.nan and row['fdate'] is np.nan:
            row['ddate'] = last_fisc_yr + relativedelta(months=3*row['seq'])
        df.loc[count, 'ddate'] = row['ddate']
    return df

def lower_columns(df):
        """
        lower all column names
        """

        cols = [col.lower() for col in df.columns]
        df.columns = cols
        return df

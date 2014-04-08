"""
Temporary place to store some functions and helpers for demos.

Author Ely M. Spears
"""
import pandas
import numpy as np

# 0. Mark a flag about whether a given record really is at the last day of month.
# 1. Convert the TotRet items into actual monthly returns.
# 2. Sort by (Identifier, Date) and join market returns.
# 3. Group by identifier and perform rolling pandas OLS.


def clean_delistings(monthly_raw_returns,
                     date_column="Date_"):
    """
    Remove records from months when they are not as-of the final available
    date in the month. Replace with NaN and move the date to the actual end
    of month date.
    """
    original_columns = monthly_raw_returns.columns.values.tolist()
    original_columns.remove(date_column)

    # First get all of the max-dates which determine the month-end dates.
    for period in ("year", "month", "day"):
        monthly_raw_returns[period] = monthly_raw_returns.Date_.map(
            lambda x: getattr(x, period)
        )
        
    monthly_raw_returns["yearmonth"] = (
        100*monthly_raw_returns["year"] + monthly_raw_returns["month"]
    )

    max_day = monthly_raw_returns.groupby("yearmonth").agg({"day":"max"})
    max_day = max_day.rename(columns={"day":"max_day"})
    monthly_raw_returns = pandas.merge(
        monthly_raw_returns, 
        max_day, 
        left_on="yearmonth", 
        right_index=True, 
        how="left"
    )

    at_max = monthly_raw_returns["day"] == monthly_raw_returns["max_day"]
    monthly_raw_returns.ix[~at_max, "TotRet"] = np.NaN

    monthly_raw_returns["AdjDate"] = monthly_raw_returns.apply(
        lambda row: row[date_column].replace(day=row["max_day"]),
        axis=1
    )
    
    return monthly_raw_returns[["AdjDate"] + original_columns]


def adjust_period_returns(monthly_raw_returns,
                          date_column="AdjDate",
                          identifier_column="Code",
                          returns_column="TotRet"):
    """
    Given a series of raw returns (gross from inception) that fall on
    month-ends, apply a transformation to turn them into period-by-period
    returns.
    """
    def helper(id_specific_dataframe):
        df = id_specific_dataframe.sort(date_column, ascending=False)
        df[returns_column] = (1.0/100.0) * df[returns_column]

        df["TotalReturnMonthly"] = (
            df[returns_column].diff(-1) /        # r_new - r_old
            (1.0 + df[returns_column].shift(-1)) # 1 + r_old
        )

        return df[[date_column, "TotalReturnMonthly"]]

    adj_returns = monthly_raw_returns.groupby(identifier_column).apply(helper)
    adj_returns = (
        adj_returns
        .reset_index()
        .drop("level_1", axis=1)
    )

    monthly_raw_returns = pandas.merge(
        monthly_raw_returns, 
        adj_returns, 
        left_on=[identifier_column, date_column],
        right_on=[identifier_column, date_column],
        how="left"
    )

    return monthly_raw_returns


def merge_fama_french_from_hdf(idc_dataframe,
                               idc_date-column="AdjDate",
                               ff_date_column="Date"):
    """
    Loads the included FF data set. Merges with adjusted dates already in the 
    csv.
    """
    ff_df = pandas.read_hdf(
        "/home/ely/.estuarial/.cache/ff_aligned_with_idc.hdf5"
    )

    ff_df[ff_date_column] = ff_df[ff_date_column].map(lambda x: x.date())

    return pandas.merge(
        idc_dataframe, 
        ff_df, 
        left_on=idc_date_column,
        right_on=ff_date_column,
        how="left"
    )


def pandas_rolling_ols(single_id_dataframe,
                       date_column="AdjDate"):
    """
    Perform rolling ols and return the columns of date-based coefficients,
    t-stats, idiosyncratic vol, etc.
    """

    
    df = (
        single_id_dataframe
        .sort(date_column, ascending=True)
        .set_index(date_column)
    )
    
    
    try:
        ols_result = pandas.ols(
            y=df["TotalReturnMonthly"] - df["RiskFreeRate"], 
            x=df["ExcessMarket"], 
            window=60, 
            min_periods=12, 
            intercept=True
        )

        beta = ols_result.beta['x']
        beta.name = "Beta"
        beta_tstat = ols_result.t_stat['x']
        beta_tstat.name = "Beta_tstat"
        df = df.join(beta).join(beta_tstat)

    except:
        df["Beta"] = np.NaN
        df["Beta_tstat"] = np.NaN
        
    return df
    




"""
Temporary place to store some functions and helpers for demos.

Author Ely M. Spears
"""
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
        df.set_index(date_column)

        adj_returns = (
            df[returns_column].diff(-1) /        # r_new - r_old
            (1.0 + df[returns_column].shift(-1)) # 1 + r_old
        )

        # Series object can't be merged ... and needs Date as index.
        adj_returns.name = "TotalReturnMonthly"
        return adj_returns

    adj_returns =  monthly_raw_returns.groupby(identifier_column).apply(helper)

    monthly_raw_returns = pandas.merge(
        monthly_raw_returns, 
        adj_returns, 
        left_on=[identifier_column, date_column],
        right_index=True,
        how="left"
    )

    return monthly_raw_returns




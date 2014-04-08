from dateutil import parser
import datetime as dt
import calendar

def parsedate(dates):
    """
    Check datetime types and convert from str to datetime if
    necessary

    :type dates: tuple
    :param dates: tuple of start and stop dates

    :rtype: list
    :return: list of datetime objects
    """
    dt_list = []
    for date in dates:

        if isinstance(date,str):
            dt_list.append(parser.parse(date))
        elif isinstance(date,dt.datetime):
            dt_list.append(date)

    return dt_list

def end_of_month(date):
    """
    Check date is the end of the month

    :type date: datetime
    :param date: a given date with year, month, and day

    :rtype: bool
    :return: truth value of end of the month

    """
    month, day = calendar.monthrange(date.year,date.month)

    eom_flag = True if day == date.day else False

    return eom_flag




def check_end(dates):
        '''[X:] results in the two following possibilities'''
        start,stop = dates

        if stop == 9223372036854775807 or stop == None:
            now = datetime.datetime.utcnow().strftime('%Y-%m-%d')
            return [start,now]
        else:
            return [start,stop]


def check_date(dates):
    dates = parsedate(check_end(dates))
    return dates



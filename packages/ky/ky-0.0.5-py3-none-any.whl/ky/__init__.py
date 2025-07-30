"""Utils to work with dates"""

__author__ = 'thorwhalen'

from datetime import timedelta
from datetime import datetime
from pytz import timezone


def function_to_convert_to_timezone_from_timezone(to_timezone, from_timezone='UTC'):
    if isinstance(to_timezone, str):
        to_timezone = timezone(to_timezone)
    if isinstance(from_timezone, str):
        from_timezone = timezone(from_timezone)

    return lambda x: from_timezone.localize(x).astimezone(to_timezone)


def mk_time_info_extractor(spec):
    """
    Returns a function that will extract information from timestamps in a dict format.
    The specification should be a list of timetuple attributes
    (see https://docs.python.org/2/library/time.html#time.struct_time) to extract,
    or a {k: v, ...} dict where v are the timetuple attributes, and k what you want to call them in the output.

    Example:
        fun = mk_time_info_extractor({'day_of_week': 'tm_wday', 'hour_of_day': 'tm_hour'})
        # assuming you defined some timestamp called t...
        print t
        print fun(t)
    2015-06-02 20:46:16.629000
    {'day_of_week': 1, 'hour_of_day': 20}
    """
    if not isinstance(spec, dict):  # if spec is not a dict, make it so
        spec = {x: x for x in spec}

    def extractor(timestamp):
        time_struct = timestamp.timetuple()
        return {k: time_struct.__getattribute__(v) for k, v in spec.items()}

    return extractor


day_of_week_strings = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']


def day_of_week_integer_to_string(day_of_week_integer):
    return day_of_week_strings[day_of_week_integer]


def daterange(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield start_date + timedelta(n)


def datetimes_ranges_defining_months(from_date, to_date):
    from_year = from_date.year
    from_month = from_date.month
    to_year = to_date.year
    to_month = to_date.month




def is_weekend(date):
    """
    Determines if the given date is a weekend.

    Parameters:
        date (datetime.date): The date to check.

    Returns:
        bool: True if the date is a weekend (Saturday or Sunday), False otherwise.

    Example:
        >>> from datetime import date
        >>> is_weekend(date(2023, 12, 2))
        True
        >>> is_weekend(date(2023, 12, 4))
        False
    """
    return date.weekday() >= 5


def next_business_day(start_date):
    """
    Calculates the next business day from the given date, skipping weekends.

    Parameters:
        start_date (datetime.date): The date from which to calculate the next business day.

    Returns:
        datetime.date: The next business day.

    Example:
        >>> from datetime import date
        >>> next_business_day(date(2023, 12, 1))  # Friday
        datetime.date(2023, 12, 4)  # Monday
    """
    from datetime import timedelta
    next_day = start_date + timedelta(days=1)
    while next_day.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        next_day += timedelta(days=1)
    return next_day


def format_date_range(start_date, end_date, date_format='%Y-%m-%d'):
    """
    Formats a date range into a readable string.

    Parameters:
        start_date (datetime.date): The start date of the range.
        end_date (datetime.date): The end date of the range.
        date_format (str): The format string to use for dates.

    Returns:
        str: A formatted string representing the date range.

    Example:
        >>> from datetime import date
        >>> format_date_range(date(2023, 1, 1), date(2023, 1, 5))
        '2023-01-01 to 2023-01-05'
    """
    return f"{start_date.strftime(date_format)} to {end_date.strftime(date_format)}"




def is_holiday(date, holidays):
    """
    Checks if a given date is a holiday based on a provided list of holiday dates.

    Parameters:
        date (datetime.date): The date to check.
        holidays (list of datetime.date): A list of dates considered as holidays.

    Returns:
        bool: True if the date is a holiday, False otherwise.

    Example:
        >>> from datetime import date
        >>> is_holiday(date(2023, 12, 25), [date(2023, 12, 25), date(2024, 1, 1)])
        True
        >>> is_holiday(date(2023, 12, 24), [date(2023, 12, 25), date(2024, 1, 1)])
        False
    """
    return date in holidays

def filter_weekdays(dates):
    """
    Filters out the weekdays from a list of dates, returning only the weekend dates.

    Parameters:
        dates (list of datetime.date): List of dates to filter.

    Returns:
        list of datetime.date: A list containing only the weekend dates.

    Example:
        >>> from datetime import date
        >>> filter_weekdays([date(2023, 12, 1), date(2023, 12, 2), date(2023, 12, 3), date(2023, 12, 4)])
        [date(2023, 12, 2), date(2023, 12, 3)]
    """
    return [date for date in dates if date.weekday() >= 5]

def add_business_days(start_date, num_days):
    """
    Adds a specified number of business days to a given date, skipping weekends.

    Parameters:
        start_date (datetime.date): The date from which to start counting.
        num_days (int): The number of business days to add.

    Returns:
        datetime.date: The date obtained after adding the specified number of business days.

    Example:
        >>> from datetime import date
        >>> add_business_days(date(2023, 12, 1), 3)  # 1st is Friday
        datetime.date(2023, 12, 6)  # Next Wednesday
    """
    from datetime import timedelta
    current_date = start_date
    added_days = 0
    while added_days < num_days:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:  # Monday to Friday are business days
            added_days += 1
    return current_date

def time_difference_in_minutes(time1, time2):
    """
    Calculates the difference in minutes between two datetime objects.

    Parameters:
        time1 (datetime.datetime): The first datetime object.
        time2 (datetime.datetime): The second datetime object.

    Returns:
        int: The difference in minutes between the two times.

    Example:
        >>> from datetime import datetime
        >>> time1 = datetime(2023, 1, 1, 12, 0)
        >>> time2 = datetime(2023, 1, 1, 14, 30)
        >>> time_difference_in_minutes(time1, time2)
        150
    """
    return int((time2 - time1).total_seconds() / 60)

# ky
Utils to work with dates

To install:	```pip install ky```

## Overview
The `ky` package provides a collection of utilities for handling and manipulating dates and times in Python. It includes functions to convert times between timezones, extract specific time information from datetime objects, iterate over ranges of dates, and more. Below are detailed descriptions and examples of how to use each function.

### Functions

#### `function_to_convert_to_timezone_from_timezone(to_timezone, from_timezone='UTC')`
Converts a datetime object from one timezone to another. By default, it converts from UTC to the specified timezone.

**Parameters:**
- `to_timezone` (str or `pytz.timezone`): The timezone to convert to.
- `from_timezone` (str or `pytz.timezone`, optional): The timezone to convert from. Defaults to 'UTC'.

**Returns:**
- A function that takes a datetime object as input and returns it converted to the specified timezone.

**Example:**
```python
from datetime import datetime
from ky import function_to_convert_to_timezone_from_timezone

convert_to_EST = function_to_convert_to_timezone_from_timezone('America/New_York')
utc_time = datetime.utcnow()
est_time = convert_to_EST(utc_time)
print(f"UTC Time: {utc_time}, EST Time: {est_time}")
```

#### `mk_time_info_extractor(spec)`
Creates a function that extracts specified components from a datetime object.

**Parameters:**
- `spec` (list or dict): Specification of the components to extract.

**Returns:**
- A function that takes a datetime object and returns a dictionary with the specified components.

**Example:**
```python
from datetime import datetime
from ky import mk_time_info_extractor

extractor = mk_time_info_extractor(['tm_year', 'tm_mon', 'tm_mday'])
now = datetime.now()
print(extractor(now))  # Output might be {'tm_year': 2023, 'tm_mon': 12, 'tm_mday': 25}
```

#### `day_of_week_integer_to_string(day_of_week_integer)`
Converts an integer representing a day of the week to its corresponding string name.

**Parameters:**
- `day_of_week_integer` (int): Integer representing the day of the week (0=Sunday, 6=Saturday).

**Returns:**
- String representing the day of the week.

**Example:**
```python
from ky import day_of_week_integer_to_string

print(day_of_week_integer_to_string(1))  # Output: 'Mon'
```

#### `daterange(start_date, end_date)`
Generates dates from `start_date` to one day before `end_date`.

**Parameters:**
- `start_date` (`datetime.date`): Start date.
- `end_date` (`datetime.date`): End date.

**Returns:**
- A generator yielding dates from start to end.

**Example:**
```python
from datetime import date
from ky import daterange

start = date(2023, 1, 1)
end = date(2023, 1, 5)
for single_date in daterange(start, end):
    print(single_date)
```

#### `datetimes_ranges_defining_months(from_date, to_date)`
Generates datetime ranges that define the start and end of each month between `from_date` and `to_date`.

**Parameters:**
- `from_date` (`datetime.datetime`): Starting datetime.
- `to_date` (`datetime.datetime`): Ending datetime.

**Returns:**
- A generator yielding tuples (start of month, end of month) for each month in the range.

**Example:**
```python
from datetime import datetime
from ky import datetimes_ranges_defining_months

start = datetime(2023, 1, 1)
end = datetime(2023, 4, 1)
for month_start, month_end in datetimes_ranges_defining_months(start, end):
    print(f"Start: {month_start}, End: {month_end}")
```

This package is designed to simplify common date and time manipulations, making it easier to handle timezones, extract date components, and iterate over date ranges.
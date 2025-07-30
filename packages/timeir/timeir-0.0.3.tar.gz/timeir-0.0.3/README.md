A few Python functions to extract data from https://time.ir .

Usage
-----
The `holiday_occasion` function will return the holiday occasion of the requested date, or `None` if the given date is not a holiday.
```Python
In [1]: from timeir import holiday_occasion

In [2]: holiday_occasion(1404, 1, 13)
Out[2]: 'جشن سیزده به در'

In [3]: holiday_occasion(1404, 1, 14)

In [4]: 
```

**Note:** This function fetches data from the time.ir website annually (one request per requested year) and caches the results for up to 3 months. See the source code for more details.

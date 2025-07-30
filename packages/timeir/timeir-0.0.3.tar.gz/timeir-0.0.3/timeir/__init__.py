__version__ = '0.0.3'
from datetime import (
    UTC as _UTC,
    datetime as _datetime,
    timedelta as _timedelta,
)
from functools import cache as _cache


def get_year_data(sh_year: int, expire_days=30 * 3) -> dict:
    """Get time.ir data for the given solar hijri year.

    The retrieved data will be cached and on reused on subsequent calls if
    it is not older than expire_days (defaults to 90 days).
    """
    from json import dumps, loads
    from pathlib import Path

    from httpx import get

    path = Path(__file__)
    file = path.parent / f'~{sh_year}.json'

    try:
        data = file.read_bytes().decode()
    except FileNotFoundError:
        j = None
    else:
        j = loads(data)
        if (
            _datetime.now(tz=_UTC)
            - _datetime.fromisoformat(j['creation_date'])
        ) < _timedelta(days=expire_days):
            return j

    try:
        j = get(
            f'https://api.time.ir/v1/event/fa/events/yearlycalendar?year={sh_year}',
            # this is currently hardcoded on time.ir, but may change in the future
            headers={'x-api-key': 'ZAVdqwuySASubByCed5KYuYMzb9uB2f7'},
        ).json()
    except Exception as e:
        if j is not None:
            from logging import warning

            warning(
                f'Returning old cache; could not retrieve time.ir data: {e!r}'
            )
            return j
        raise

    file.write_bytes(
        dumps(
            j,
            ensure_ascii=False,
            check_circular=False,
            indent='\t',
        ).encode()
    )
    return j


@_cache
def get_holidays(sh_year: int) -> list[dict[int, str] | None]:
    """Return a list of mappings of day int to holiday title for each month.

    The first element of the list is always None.
    There will be 12 dicts in the list.
    """
    holidays: list[dict | None] = [None]
    append = holidays.append
    j = get_year_data(sh_year)
    for month_data in j['data']:
        month_holidays = {}
        append(month_holidays)
        for event in month_data['event_list']:
            if event['is_holiday'] is not True:
                continue
            month_holidays[event['jalali_day']] = event['title']
    return holidays


def holiday_occasion(sh_year, sh_month, sh_day) -> str | None:
    return get_holidays(sh_year)[sh_month].get(sh_day)

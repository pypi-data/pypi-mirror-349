import datetime
import logging
import pandas as pd
import pytz
import re
from tzlocal import get_localzone

from contexere import __month_dict__, __day_dict__, __hours__
from contexere import __pattern__ as schematic
from contexere.discover import build_context, last


def abbreviate_date(date=None, tz=pytz.utc, local=False,
                    month=__month_dict__, day=__day_dict__):
    if date is None:
        if local:
            date = datetime.datetime.now(tz=get_localzone())
        else:
            date = datetime.datetime.now(tz=tz)
    elif type(date) == str:
        date = pd.Timestamp(date)
    year = date.strftime('%y')

    return year + month[date.month] + day[date.day]


def abbreviate_time(date=None, seconds=False, tz=pytz.utc,  local=False, hour=__hours__):
    if date is None:
        if local:
            date = datetime.datetime.now(tz=get_localzone())
        else:
            date = datetime.datetime.now(tz=tz)
    elif type(date) == str:
        date = pd.Timestamp(date)
    abbr = hour[date.hour] + '{:02}'.format(date.minute)
    if seconds:
        return abbr + '{:02}'.format(date.second)
    return abbr


def abbreviate_datetime(date=None, seconds=False, tz=pytz.utc, local=False):
    if date is None:
        date = datetime.datetime.now(tz=tz)
    return abbreviate_date(date, local=local) + abbreviate_time(date,
                                                                seconds=seconds,
                                                                local=local)


def decode_abbreviated_datetime(abrv, tz=pytz.utc):
    """
    Decode the 2021 naming scheme to a datetime object

    Args:
        abrv: String in format yymd[hMM]
              yy [0-9][0-9] encodes the years 2000 to 2099
              m [o-z] encodes the months with 'o' referring to January and
                                              'z' referring to December
              d [1-9,A-V] encodes the day, which is either the number, or
                                                            'A' referring to the 10th,
                                                        and 'V' referring to the 31st
              h [a-x] encodes the hour with 'a' referring to midnight and 'x' to 23
              MM [0-5][0-9] encodes the minutes 0 to 59
        tz: time zone info (default: pytz.utc)

    Returns: datetime object
    """
    assert len(abrv) == 4 or len(abrv) == 7
    year = int(abrv[:2]) + 2000
    month = ord(abrv[2]) - ord('o') + 1
    if abrv[3] in list(map(chr, range(ord('1'), ord('9') + 1))):
        day = int(abrv[3])
    else:
        day = ord(abrv[3]) - ord('A') + 10
    if len(abrv) == 7:
        hour = ord(abrv[4]) - ord('a')
        minutes = int(abrv[-2:])
    else:
        hour = 0
        minutes = 0
    return datetime.datetime(year, month, day, hour, minutes, tzinfo=tz)


def suggest_next(directory='.', project=None, local=True):
    context, timeline = build_context(directory, project_filter=project)
    logging.info('Projects' + str(list(context.keys())))
    logging.info('Timeline' + str(list(timeline.keys())))
    today = abbreviate_date(local=local)
    if len(timeline) == 0:
        if project is None:
            raise ValueError(f"No project files matching the naming scheme found in path {directory}"
                             "and option '--project' wasn't set.")
        else:
            this_project = project
            next_step = 'a'
    else:
        latest = last(timeline)
        match = schematic.match(latest[0])
        this_project = match.group('project')
        if today == match.group('date'):
            assert match.group('step') != 'z'
            next_step = chr(ord(match.group('step')) + 1)
        else:
            next_step = 'a'
    suggestion = this_project + today + next_step
    return suggestion

def next_month_start(this_year, this_month, datetime=True):
    """
    Return abbreviation for the start of next month.

    This function is useful if data were collected for a specific month and
    the timestamp is supposed to indicate the end of the period.

    Args:
        this_year: Year of data collection
        this_month: Month of data collection
        datetime: Boolean indicating if timestamp is generated with time (default: True) or without

    Returns:
        String with abbreviated timestamp
    """
    assert this_month >= 1 and this_month <= 12
    if this_month <= 11:
        month = this_month + 1
        year = this_year
    else:
        month = 1
        year = this_year + 1
    t = pd.Timestamp(year=year, month=month, day=1, hour=0, minute=0)
    if datetime:
        return abbreviate_datetime(t)
    else:
        return abbreviate_date(t)
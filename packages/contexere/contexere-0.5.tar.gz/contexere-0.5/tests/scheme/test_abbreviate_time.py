from datetime import datetime
import pytz

from contexere.scheme import abbreviate_time

def test_midnight():
    dt = datetime(2022, 1, 1, 0, 0)
    assert abbreviate_time(dt) == 'a00'
    assert abbreviate_time(dt, seconds=True) == 'a0000'

    dt = datetime(2022, 1, 1, 1, 42)
    assert abbreviate_time(dt) == 'b42'
    assert abbreviate_time(dt, seconds=True) == 'b4200'

def test_arbitrary_time():
    dt = datetime(2022, 1, 19, 5, 54)
    assert abbreviate_time(dt) == 'f54'

def test_time_zone_agnostic():
    dt = datetime(2022, 1, 19, 5, 54, tzinfo=pytz.timezone("Pacific/Auckland"))
    assert abbreviate_time(dt) == 'f54'

def test_string_input():
    assert abbreviate_time('2022-04-03 23:00') == 'x00'

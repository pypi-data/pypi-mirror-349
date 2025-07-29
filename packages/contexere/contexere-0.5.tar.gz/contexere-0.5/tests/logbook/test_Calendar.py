from datetime import datetime
import pytz

from contexere.logbook import Calendar

def test_day_only():
    calendar = Calendar()
    assert calendar['22pM'] == datetime(2022, 2, 22, tzinfo=pytz.timezone('UTC'))

def test_datetime():
    calendar = Calendar()
    assert calendar['22oJf00'] == datetime(2022, 1, 19, 5, tzinfo=pytz.timezone('UTC'))

def test_datetime_with_seconds():
    calendar = Calendar()
    assert calendar['22oJf53'] == datetime(2022, 1, 19, 5, 53, tzinfo=pytz.timezone('UTC'))

def test_midnight():
    calendar = Calendar()

    dt = datetime(2022, 1, 1, 0, 0)
    assert calendar(dt) == '22o1a00'

    dt = datetime(2022, 1, 1, 1, 42)
    assert calendar(dt) == '22o1b42'

def test_arbitrary_time():
    calendar = Calendar()
    dt = datetime(2022, 1, 19, 5, 54)

    assert calendar(dt) == '22oJf54'

def test_time_zone_agnostic():
    calendar = Calendar()
    dt = datetime(2022, 1, 19, 5, 54, tzinfo=pytz.timezone("Pacific/Auckland"))

    assert calendar(dt) == '22oJf54'
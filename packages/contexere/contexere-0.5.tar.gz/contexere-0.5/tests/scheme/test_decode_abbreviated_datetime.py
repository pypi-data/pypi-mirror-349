from datetime import datetime
import pytz

from contexere.scheme import decode_abbreviated_datetime

def test_day_only():
    assert decode_abbreviated_datetime('22pM') == datetime(2022, 2, 22, tzinfo=pytz.timezone('UTC'))

def test_datetime():
    assert decode_abbreviated_datetime('22oJf00') == datetime(2022, 1, 19, 5, tzinfo=pytz.timezone('UTC'))

def test_datetime_with_seconds():
    assert decode_abbreviated_datetime('22oJf53') == datetime(2022, 1, 19, 5, 53, tzinfo=pytz.timezone('UTC'))

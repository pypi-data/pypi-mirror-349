from datetime import datetime

from contexere.scheme import abbreviate_date

def test_first_day_of_month():
    day = datetime(2022, 1, 1)
    assert abbreviate_date(day) == '22o1'

def test_last_day_of_month_with_31_days():
    day = datetime(2022, 1, 31)
    assert abbreviate_date(day) == '22oV'

def test_last_day_of_February():
    day = datetime(2022, 2, 28)
    assert abbreviate_date(day) == '22pS'

def test_last_day_of_February_in_leap_year():
    day = datetime(2020, 2, 29)
    assert abbreviate_date(day) == '20pT'

def test_last_day_of_April():
    day = datetime(2022, 4, 30)
    assert abbreviate_date(day) == '22rU'

def test_number_character_transition():
    day = datetime(2022, 4, 9)
    assert abbreviate_date(day) == '22r9'

    day = datetime(2022, 4, 10)
    assert abbreviate_date(day) == '22rA'

def test_string_input():
    assert abbreviate_date('2022-04-03 23:00') == '22r3'

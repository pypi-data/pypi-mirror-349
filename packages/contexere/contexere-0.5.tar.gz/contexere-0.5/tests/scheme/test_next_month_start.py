import pytest

from contexere.scheme import next_month_start

def test_next_month_with_datetime():
    with pytest.raises(AssertionError):
        next_month_start(2024, 0)
        next_month_start(2024, 13)

    assert next_month_start(2024, 1) == '24p1a00'
    assert next_month_start(2024, 12) == '25o1a00'

def test_next_month_without_datetime():
    with pytest.raises(AssertionError):
        next_month_start(2024, 0, datetime=False)
        next_month_start(2024, 13, datetime=False)

    assert next_month_start(2024, 1, datetime=False) == '24p1'
    assert next_month_start(2024, 12, datetime=False) == '25o1'

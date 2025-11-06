from app.logic import calculate_minutes_late


def test_on_time():
    assert calculate_minutes_late('06:00') == 0


def test_late_45():
    assert calculate_minutes_late('06:45') == 45


def test_before_time():
    assert calculate_minutes_late('05:30') == 0


def test_none():
    assert calculate_minutes_late(None) == 0

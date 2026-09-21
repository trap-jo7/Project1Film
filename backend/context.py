"""Cultural calendar + time-of-day helpers."""
from datetime import datetime


def cultural_event(now: datetime) -> str | None:
    m, d = now.month, now.day
    if m == 10:
        return "spooky_season"
    if m == 12 and d >= 10:
        return "holiday_season"
    if m == 12 or (m == 1 and d <= 5):
        return "cozy_winter"
    if m == 2 and 10 <= d <= 16:
        return "valentines"
    if m in (2, 3) and d < 15:
        return "awards_season"
    if m in (6, 7, 8):
        return "summer_blockbuster"
    if m in (4, 5):
        return "spring_indie"
    return None


def time_of_day(now: datetime) -> str:
    h = now.hour
    if 5 <= h < 11:
        return "morning"
    if 11 <= h < 17:
        return "afternoon"
    if 17 <= h < 21:
        return "evening"
    return "late_night"

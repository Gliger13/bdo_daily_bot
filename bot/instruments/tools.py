from datetime import datetime, timedelta
import json
import os


def get_sec_left(time_end: str) -> int:
    hours_end, minutes_end = tuple(map(int, time_end.split(':')))
    time_start = datetime.now()
    delta_start = timedelta(hours=time_start.hour, minutes=time_start.minute, seconds=time_start.second)
    delta_end = timedelta(hours=hours_end, minutes=minutes_end)
    delta_left = delta_end - delta_start
    return delta_left.seconds


def get_time_difference(time_start, time_end) -> int:
    delta_start = datetime.strptime(time_start, '%H:%M')
    delta_end = datetime.strptime(time_end, '%H:%M')
    return (delta_end - delta_start).seconds

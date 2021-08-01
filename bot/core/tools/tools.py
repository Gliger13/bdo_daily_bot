"""
Contain difference common functions. Will be separated and removed
"""
from datetime import datetime


def get_time_difference(time_start, time_end) -> int:
    delta_start = datetime.strptime(time_start, '%H:%M')
    delta_end = datetime.strptime(time_end, '%H:%M')
    return (delta_end - delta_start).seconds

from datetime import datetime, timedelta


class MetaSingleton(type):
    """
    Realize pattern Singleton
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def get_sec_left(time_end: str) -> int:
    """
    Return seconds left from now
    """
    hours_end, minutes_end = tuple(map(int, time_end.split(':')))
    time_start = datetime.now()
    delta_start = timedelta(hours=time_start.hour, minutes=time_start.minute, seconds=time_start.second)
    delta_end = timedelta(hours=hours_end, minutes=minutes_end)
    delta_left = delta_end - delta_start
    return delta_left.seconds


def now_time_plus_minute() -> str:
    now_plus_1 = datetime.now() + timedelta(minutes=1)
    now_time_plus_1 = timedelta(hours=now_plus_1.hour, minutes=now_plus_1.minute)
    return ':'.join(str(now_time_plus_1).split(':')[:-1])


def get_time_difference(time_start, time_end) -> int:
    delta_start = datetime.strptime(time_start, '%H:%M')
    delta_end = datetime.strptime(time_end, '%H:%M')
    return (delta_end - delta_start).seconds


def validate_time(time_to_display):
    # Convert in timedelta
    time_list = []
    last_time = datetime.strptime(time_to_display[0], '%H:%M')
    last_time = timedelta(hours=last_time.hour, minutes=last_time.minute)
    for time_index, time in enumerate(time_to_display[1:]):
        time = datetime.strptime(time, '%H:%M')
        time = timedelta(hours=time.hour, minutes=time.minute)

        if time < last_time:
            for next_day_time in time_to_display[time_index + 1:]:
                some_time = datetime.strptime(next_day_time, '%H:%M')
                some_time = timedelta(hours=some_time.hour, minutes=some_time.minute)
                time_list.append(some_time + timedelta(days=1))
            break
        else:
            time_list.append(time)

        last_time = time
    return time_list

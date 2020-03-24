from datetime import datetime, timedelta
from pymongo import MongoClient
import time


def get_sec_left(time_end: str) -> int:
    hours_end, minutes_end = tuple(map(int, time_end.split(':')))
    time_start = datetime.now()
    delta_start = timedelta(hours=time_start.hour, minutes=time_start.minute, seconds=time_start.second)
    delta_end = timedelta(hours=hours_end, minutes=minutes_end)
    delta_left = delta_end - delta_start
    return delta_left.seconds


def print_log(user, msg_command, result: bool):
    print(f"{time.ctime()[-13:]}\tПользователь {user} использовал команду {msg_command}. {result}")


def raid_table_in_time(time_leaving: str) -> iter:
    """Return list time for table display"""
    sec_left = get_sec_left(time_leaving)
    half_sec_inter = sec_left // 2
    show_time_list = [half_sec_inter//4 for i in range(4)]
    show_time_list.append(half_sec_inter // 2)
    show_time_list.append(half_sec_inter // 2)
    return show_time_list


if __name__ == '__main__':
    pass

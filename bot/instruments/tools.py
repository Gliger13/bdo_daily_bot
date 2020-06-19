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


def raid_table_in_time(time_leaving: str) -> iter:
    """Return list time for table display"""
    sec_left = get_sec_left(time_leaving)
    half_sec_inter = sec_left // 2
    show_time_list = [half_sec_inter//4 for i in range(4)]
    show_time_list.append(half_sec_inter // 2)
    show_time_list.append(half_sec_inter // 2)
    return show_time_list


def save_channels(channels: dict):
    with open('settings/correct_channels.json', 'w') as save_file:
        json.dump(channels, save_file)


def save_not_dell_msgs(msgs: dict):
    with open('settings/not_dell_msgs.json', 'w') as save_file:
        json.dump(msgs, save_file)


def load_channels():
    if not os.path.exists('settings/correct_channels.json'):
        return {}
    with open('settings/correct_channels.json', 'r') as load_file:
        channels = json.load(load_file)
    if not channels:
        return {}
    return channels


def load_not_dell_msgs():
    if not os.path.exists('settings/not_dell_msgs.json'):
        return {}
    with open('settings/not_dell_msgs.json', 'r') as load_file:
        not_dell_msgs = json.load(load_file)
    if not not_dell_msgs:
        not_dell_msgs = {}
    return not_dell_msgs



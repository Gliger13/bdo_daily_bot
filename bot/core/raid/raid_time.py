"""
Contain class for storing and processing raid time
"""
from datetime import datetime, timedelta
from typing import List


class RaidTime:
    """
    Class for storing and processing raid time
    """
    __time_to_wait_after_leaving = timedelta(minutes=10)
    __time_to_notify_before_leaving = timedelta(minutes=7)

    def __init__(self, time_leaving: datetime, time_reservation_open: datetime):
        """
        :param time_leaving: time when raid leaving
        :param time_reservation_open: time when starts reservation places in raid
        """
        self.time_leaving = time_leaving
        self.time_reservation_open = time_reservation_open
        self.creation_time = None

        self.secs_to_display_list = self.__set_secs_list_before_display()

    @property
    def kebab_time_leaving(self) -> str:
        """
        Gets raid time leaving in kebab format, e.g. 19-00

        :return: raid time leaving in kebab format
        """
        return self.time_leaving.strftime('%H-%M')

    @property
    def kebab_time_reservation_open(self) -> str:
        """
        Gets raid time reservation open in kebab format, e.g. 19-00

        :return: raid time leaving in kebab format
        """
        return self.time_reservation_open.strftime('%H-%M')

    @property
    def normal_time_leaving(self) -> str:
        """
        Gets raid time leaving in human format, e.g. 19:00

        :return: raid time leaving in human format
        """
        return self.time_leaving.strftime('%H:%M')

    @property
    def normal_time_reservation_open(self) -> str:
        """
        Gets raid time reservation open in human format, e.g. 19:00

        :return: raid time leaving in human format
        """
        return self.time_reservation_open.strftime('%H:%M')

    @property
    def normal_next_display_time(self) -> str:
        """
        Returns next time to display in human format

        :return: raid time leaving in human format
        """
        if self.secs_to_display_list:
            return (datetime.now() + timedelta(seconds=self.secs_to_display_list[-1])).strftime('%H:%M')
        return self.kebab_time_leaving

    @property
    def normal_time_channel_deleting(self) -> str:
        """
        Returns time when raid channel will be deleted in human format

        :return: time when raid channel will be deleted in human format
        """
        return (self.time_leaving + self.__time_to_wait_after_leaving).strftime('%H:%M')

    @property
    def secs_before_collection(self) -> int:
        """
        Returns seconds before raid start collection

        :return: seconds before collection
        """
        return int((self.time_reservation_open - datetime.now()).total_seconds())

    @property
    def secs_after_leaving(self) -> int:
        """
        Returns seconds after raid left

        :return: seconds after raid left
        """
        return int(self.__time_to_wait_after_leaving.total_seconds())

    @property
    def time_to_notify(self) -> datetime:
        """
        Return time where raid members should be notified
        """
        return self.time_leaving - self.__time_to_notify_before_leaving

    @property
    def secs_before_notification(self) -> float:
        """
        Return seconds before time raid members notification
        """
        return (self.time_to_notify - datetime.now()).total_seconds()

    def get_secs_to_display_generator(self) -> int:
        """
        Returns generator that returns seconds to next display

        :return: seconds to next display
        """
        for _ in range(len(self.secs_to_display_list)):
            yield self.secs_to_display_list[-1]
            self.secs_to_display_list.pop()

    def __set_secs_list_before_display(self) -> List[int]:
        """
        Gets list of seconds before display

        Gets list of seconds before 1, 5, 15, 30, 60 and 1 hours before display
        """
        secs_to_display_list = []
        time_difference = self.time_leaving - datetime.now()
        if time_difference.total_seconds() < 0:
            return secs_to_display_list
        time_difference_seconds = time_difference.total_seconds()

        # If difference is greater then a minute display at 1 minute before leaving and moment of leaving
        if time_difference_seconds > 60:
            secs_to_display_list.append(60)
            time_difference_seconds -= 60
        # If difference is less then a minute then just wait it
        else:
            secs_to_display_list.append(time_difference_seconds)
        # If difference is greater then a 5 minutes display at 5 minutes before leaving
        if time_difference_seconds > 300:
            secs_to_display_list.append(300)
            time_difference_seconds -= 300
        # If difference is greater then a 15 minutes display at 15 minutes before leaving
        if time_difference_seconds > 600:
            secs_to_display_list.append(600)
            time_difference_seconds -= 600
        # If difference is greater then a 30 minutes display at 30 minutes before leaving
        if time_difference_seconds > 900:
            secs_to_display_list.append(900)
            time_difference_seconds -= 900
        # If difference is greater then a 60 minutes display at 60 minutes before leaving
        if time_difference_seconds > 1800:
            secs_to_display_list.append(1800)
            time_difference_seconds -= 1800
        hours_left_to_display = int(time_difference_seconds // 3600)
        if hours_left_to_display:
            for _ in range(hours_left_to_display):
                secs_to_display_list.append(3600)
            time_difference_seconds -= hours_left_to_display * 3600
        secs_to_display_list[-1] += time_difference_seconds
        return secs_to_display_list

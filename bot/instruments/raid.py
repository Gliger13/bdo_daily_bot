import datetime
import json
import os
import random
from datetime import datetime, timedelta

import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image


class Raid:
    """
    Create Raid Object that contain members amount of members and etc

    """
    def __init__(self,
                 captain_name, server, time_leaving, time_reservation_open, guild_id, channel_id, reservation_count=2
                 ):
        # Info about BDO raid
        self.captain_name = captain_name
        self.member_dict = {}
        self.server = server
        self.raid_time = RaidTime(time_leaving, time_reservation_open)
        self.reservation_count = max(int(reservation_count), 1)

        self.members_count = self.reservation_count
        self.table = None

        self.guild_id = guild_id
        self.channel_id = channel_id
        self.collection_msg = None
        self.table_msg = None

        self.is_delete_raid = False
        self.collection_task = None
        self.task_list = []
        current_time = datetime.now()
        self.time_of_creation = f'{current_time.hour}-{current_time.minute}-{current_time.second}'

    @property
    def places_left(self):
        return 20 - self.members_count

    def __iadd__(self, name_new_member):
        if self.places_left == 0:
            return False
        self.members_count += 1
        self.member_dict.update({name_new_member: self.members_count})
        return self

    def __isub__(self, name_remove_member):
        if self.member_dict.get(name_remove_member):
            del self.member_dict[name_remove_member]
            self.members_count -= 1
            return self
        else:
            return False

    def __cmp__(self, other):
        if self.members_count > other.members_count:
            return 1
        elif self.members_count == other.members_count:
            return 0
        else:
            return -1

    def __lt__(self, other):
        return self.members_count < other.members_count

    def __gt__(self, other):
        return self.members_count > other.members_count

    def table_path(self) -> str:
        if not self.table:
            self.table = Table(self)
            self.table.create_table()
        else:
            self.table.update_table(self)
        return self.table.table_path

    def save_raid(self):
        raid_information = {
            "captain_name": self.captain_name,
            "server": self.server,
            "time_leaving": self.raid_time.time_leaving,
            "time_reservation_open": self.raid_time.time_reservation_open,
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "reservation_count": self.reservation_count,
            "time_to_display": self.raid_time.time_to_display,
            "secs_to_display": self.raid_time.secs_to_display,
            "members_dict": self.member_dict,
            "members_count": self.members_count,
        }
        # Find dir 'saves'. If not - create
        for file in os.listdir(path='.'):
            if file == 'saves':
                break
        else:
            os.mkdir('saves')
        # Save raid in txt file
        file_name = f"saves/{self.captain_name}_{'-'.join(self.raid_time.time_leaving.split(':'))}.json"
        with open(file_name, 'w', encoding='utf-8') as save_file:
            json.dump(raid_information, save_file)


class RaidTime:
    DISPLAY_FREQUENCY = 4  # times
    NOTIFY_BEFORE_LEAVING = timedelta(minutes=7)
    # Display n minutes before leaving
    DISPLAY_BEFORE_LEAVING = [
        timedelta(minutes=15),
        timedelta(minutes=5),
    ]
    MIN_TIME_DISPLAY = timedelta(seconds=60)

    def __init__(self, time_leaving, time_reservation_open):
        self.creation_time = datetime.now()
        self.time_to_display = []
        self.secs_to_display = []
        self.time_leaving = time_leaving
        self.time_reservation_open = time_reservation_open

        self.notification_task = None
        self.is_notified = False  # Have users received an notification?

        self._time_leaving = datetime.strptime(time_leaving, '%H:%M')
        self._time_reservation_open = datetime.strptime(time_reservation_open, '%H:%M')

        self._set_intervals()

    @property
    def _additional_time(self):
        if self.DISPLAY_BEFORE_LEAVING:
            time_list = list(reversed(sorted(self.DISPLAY_BEFORE_LEAVING)))
            last_time = time_list.pop(0)
            time_before_next = []
            for current_time in time_list:
                time_before_next.append(last_time - current_time)
                last_time = current_time
            time_before_next.append(last_time)
            return time_before_next
        else:
            return []

    def remove_previous_time(self):
        self.time_to_display.pop(0)
        self.secs_to_display.pop(0)

    @staticmethod
    def _clear_additional_time(time_list, interval_part):
        """
        Remove time from time_list that greater than interval_part
        """
        return [time for time in time_list if time < interval_part]

    def validate_time(self):
        # Convert in timedelta
        current_datetime = datetime.now()
        current_time = timedelta(hours=current_datetime.hour, minutes=current_datetime.minute)

        if current_time < timedelta(hours=self._time_reservation_open.hour, minutes=self._time_reservation_open.minute):
            current_time += timedelta(days=1)

        # Convert in timedelta
        last_time = datetime.strptime(self.time_to_display[0], '%H:%M')
        last_time = timedelta(hours=last_time.hour, minutes=last_time.minute)

        for time_index, time in enumerate(self.time_to_display[1:]):
            # Convert in timedelta
            time = datetime.strptime(time, '%H:%M')
            time = timedelta(hours=time.hour, minutes=time.minute)

            if last_time > time:
                time += timedelta(days=1)
            last_time = time
            if not current_time > time:
                self.time_to_display = self.time_to_display[time_index + 1:]
                self.secs_to_display = self.secs_to_display[time_index + 1:]
                break

    def _set_intervals(self):
        display_frequency = self.DISPLAY_FREQUENCY

        # Correct the time if the time leaving is the next day
        if self._time_reservation_open > self._time_leaving:
            interval = self._time_leaving + timedelta(days=1) - self._time_reservation_open
        else:
            interval = self._time_leaving - self._time_reservation_open

        # Reduce the frequency of display if the interval is not enough
        if interval < self.MIN_TIME_DISPLAY * display_frequency:
            display_frequency = interval // self.MIN_TIME_DISPLAY // 2

        interval_part = interval / display_frequency if display_frequency else interval
        # Take time for a specific display
        additional_list = self._clear_additional_time(self._additional_time, interval_part)

        # Calculate min_interval
        # 1 minute for compensate the time spent on computing
        min_interval = self.MIN_TIME_DISPLAY * display_frequency + timedelta(minutes=1)

        for display_time in additional_list:
            min_interval += display_time

        # do not display if the interval is small
        if interval > min_interval and additional_list and interval_part > max(additional_list):
            can_additionally_display = True
            interval -= max(additional_list)
        else:
            can_additionally_display = False

        interval_part = interval / display_frequency if display_frequency else interval

        # Structure of all time interval like this
        # [__.__, __.__, __.__, __.__, *additional_time, _time_leaving]
        # where . is time to display

        self.secs_to_display.append((interval_part // 2).total_seconds())
        for part in range(display_frequency - 1):
            self.secs_to_display.append(interval_part.total_seconds())
        self.secs_to_display.append((interval_part // 2).total_seconds())

        time_to_display = self._time_reservation_open
        for interval_part_secs in self.secs_to_display:
            time_to_display += timedelta(seconds=interval_part_secs)
            str_time = time_to_display.strftime('%H:%M')
            self.time_to_display.append(str_time)

        # Add additional time to display
        if can_additionally_display:
            for additional_time in additional_list:
                time_to_display = self._time_leaving - additional_time
                str_time = time_to_display.strftime('%H:%M')
                self.time_to_display.append(str_time)
                self.secs_to_display.append(additional_time.total_seconds())

        # Add display at time leaving
        self.time_to_display.append(self._time_leaving.strftime('%H:%M'))
        # Remove duplicate items from list
        self.time_to_display = list(dict.fromkeys(self.time_to_display))

    def _is_time_to_notify(self):
        if sum(self.secs_to_display[1:]) < self.NOTIFY_BEFORE_LEAVING.total_seconds() and not self.is_notified:
            return True
        else:
            return False

    def secs_to_notify(self) -> float or None:
        if self._is_time_to_notify():
            return sum(self.secs_to_display) - self.NOTIFY_BEFORE_LEAVING.total_seconds()


class Table:
    # Text settings

    # Size
    HEIGHT = 420

    # For text
    TEXT_FONT_SIZE = 18  # pt
    # Font path
    FONT_PATH = os.path.join("settings", "font_table.ttf")
    # Set font size and encoding
    FONT = ImageFont.truetype(FONT_PATH, TEXT_FONT_SIZE, encoding="UTF-8")

    # For numbers of columns
    NUMBER_FONT_SCALE = 0.5  # Font scale factor that is multiplied by the font-specific base size.
    NUMBER_FONT_FACE = cv2.FONT_HERSHEY_DUPLEX
    NUMBER_COLOR = (25, 25, 25)  # rgb
    NUMBER_THICKNESS = 1
    NUMBER_BASE_LINE = cv2.LINE_AA
    # '0000' - space that takes for number of member
    NUMBER_SIZE = cv2.getTextSize('0000', NUMBER_FONT_FACE, NUMBER_FONT_SCALE, NUMBER_THICKNESS)
    NUMBER_SIZE_WIDTH = NUMBER_SIZE[0][0]  # px

    # Table frame
    COLUMNS = 21
    LINE_WIDTH = 1

    def __init__(self, raid: Raid):
        self.raid = raid
        self.old_member_dict = self.raid.member_dict.copy()
        self.title = f"{self.raid.captain_name} {self.raid.server} {self.raid.raid_time.time_leaving}"
        self.table_path = None

    def get_width(self):
        # 15 - 15px - offset the indent
        title_width = Table.FONT.getsize(self.title)[0] + 15
        if self.raid.member_dict:
            max_name = max(self.raid.member_dict)
            max_name_row_width = Table.NUMBER_SIZE_WIDTH + Table.FONT.getsize(max_name)[0]
            return max(title_width - 10, max_name_row_width)
        return title_width

    def create_table(self):
        width = self.get_width()
        # Build frame of table
        # Create white image
        img = np.zeros((Table.HEIGHT, width, 3), np.uint8)
        img[::, ::] = 255

        # Draw reservation red space
        start_point = (0, Table.HEIGHT)
        end_point = (width, Table.HEIGHT - Table.HEIGHT // Table.COLUMNS * self.raid.reservation_count)
        color = (0, 0, 255)
        rect_thickness = -1  # Thickness of -1 px will fill the rectangle shape by the specified color
        cv2.rectangle(img, start_point, end_point, color, rect_thickness)

        # Draw lines of table
        for number in range(21):
            # Set bottom left and top right coordinate of 21 rectangles
            start_point = 0, (Table.HEIGHT // Table.COLUMNS) * (number + 1)
            end_point = width - Table.LINE_WIDTH // 2, (Table.HEIGHT // Table.COLUMNS) * number
            # Set coordinate of numerations
            point_number = 2, (Table.HEIGHT // Table.COLUMNS) * (number + 1) - 4
            # Draw 21 rectangles
            cv2.rectangle(img, start_point, end_point, (0, 0, 0), Table.LINE_WIDTH)
            if number > 0:  # Draw numeration of 20 columns
                cv2.putText(
                    img=img,
                    text=str(number),
                    org=point_number,
                    fontFace=Table.NUMBER_FONT_FACE,
                    fontScale=Table.NUMBER_FONT_SCALE,
                    color=Table.NUMBER_COLOR,
                    thickness=Table.NUMBER_THICKNESS,
                    lineType=Table.NUMBER_BASE_LINE,
                )

        # Draw vertical line... Yes its rectangle, not line but line
        start_point = (0, Table.HEIGHT)
        end_point = (30, 0)
        color = (0, 0, 0)
        rect_thickness = 1
        cv2.rectangle(img, start_point, end_point, color, rect_thickness)

        # Create random color block in top title
        start_point = (0, Table.HEIGHT // Table.COLUMNS)
        end_point = (width, 0)
        # RGB(..., ..., ...). ... - [0: 255]. For readability exclude absolute white and black colors
        color_title = (random.randrange(30, 230), random.randrange(30, 230), random.randrange(30, 230))
        rect_thickness = -1
        cv2.rectangle(img, start_point, end_point, color_title, rect_thickness)

        # Writing text on table
        # Change type to work with Pillow
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        # Fill table by members list
        name_number = 0
        for name in self.raid.member_dict:
            # Set coordinate of text message
            point_name = 35, (Table.HEIGHT // Table.COLUMNS * (name_number + 1))
            draw.text(point_name, name, font=Table.FONT, fill=(0, 0, 0, 0))
            name_number += 1

        # Draw name of captain in title
        draw.text((5, 0), self.title, font=Table.FONT, fill=(0, 0, 0, 0))

        # Changing type back into NumPy array
        img = np.array(img_pil)

        self._save(img)
        return self.table_path

    def update_table(self, raid: Raid):
        if not self.old_member_dict == raid.member_dict:
            self.__init__(raid)
            self.old_member_dict = raid.member_dict.copy()
            self.create_table()
        else:
            return

    def _save(self, img):
        # Save image on local storage
        # Find dir 'images'. If not - create
        for file in os.listdir():
            if file == 'images':
                break
        else:
            os.mkdir('images')

        self.table_path = os.path.join('images', 'raid_') + str(self.raid.raid_time.time_leaving) + ".png"
        cv2.imwrite(self.table_path, img)

    def create_text_table(self):
        table = self.title
        for name in self.raid.member_dict:
            table += f"{name}\n"
        return table

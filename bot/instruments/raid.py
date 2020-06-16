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
    def __init__(self, ctx, captain_name, server, time_leaving, time_reservation_open, reservation_count=2):
        # Info about BDO raid
        self.captain_name = captain_name
        self.member_dict = {}
        self.server = server
        self.time_leaving = time_leaving
        self.time_reservation_open = time_reservation_open
        self.reservation_count = max(int(reservation_count), 1)

        self.members_count = self.reservation_count
        self.table = None

        self.guild_id = ctx.guild.id
        self.channel_id = ctx.channel.id
        self.collection_msg = None
        self.table_msg = None

        self.time_to_display = []
        self.is_delete_raid = False
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

    def time_left_to_display(self) -> (iter, iter):
        hours_end, minutes_end = tuple(map(int, self.time_leaving.split(':')))
        time_start = datetime.now()
        delta_one_day = timedelta(days=1)
        delta_start = timedelta(hours=time_start.hour, minutes=time_start.minute, seconds=time_start.second)
        delta_end = timedelta(hours=hours_end, minutes=minutes_end)
        # Calculation seconds interval
        seconds_left = (delta_end - delta_start if delta_end > delta_start
                        else (delta_end + delta_one_day) - delta_start).total_seconds()
        half_inter = seconds_left // 2
        sec_to_display = [half_inter // 4 for i in range(4)]
        sec_to_display.append(half_inter // 2)
        sec_to_display.append(half_inter // 2)
        sec_to_display = list(map(int, sec_to_display))
        # Calculation hh:mm interval and set value to return
        sec_show = delta_start.total_seconds()
        for sec in sec_to_display:
            sec_show += sec
            hh = int(sec_show // 3600 if sec_show // 3600 < 24 else sec_show // 3600 - 24)
            mm = int((sec_show / 3600 - hh) * 60 if sec_show / 3600 < 24 else (sec_show / 3600 - hh - 24) * 60)
            hh_mm = f'{hh}:{mm}' if len(str(mm)) == 2 else f'{hh}:0{mm}'
            self.time_to_display.append((sec, hh_mm))
        return self.time_to_display

    def make_valid_time(self):
        # not good solution for problem but valid solution
        # remake in Raid.method
        # Get time_reservation_open in sec:
        hours_open, minutes_open = tuple(map(int, self.time_reservation_open.split(':')))
        res_open = timedelta(hours=hours_open, minutes=minutes_open)
        sec_open = res_open.total_seconds()

        time_now = datetime.now()
        sec_now = timedelta(hours=time_now.hour, minutes=time_now.minute, seconds=time_now.second).total_seconds()

        if sec_now < sec_open:
            sec_now += 24 * 60 * 60
        new_time_to_display = []
        all_sec_left = 0
        for sec_left, time_display in self.time_to_display:
            if not sec_left and not time_display:
                continue
            all_sec_left += sec_left
            if not sec_now > sec_open + all_sec_left:
                new_time_to_display.append((sec_left, time_display))
        return new_time_to_display

    def save_raid(self):
        raid_information = {
            "captain_name": self.captain_name,
            "server": self.server,
            "time_leaving": self.time_leaving,
            "time_reservation_open": self.time_reservation_open,
            "reservation_count": self.reservation_count,
            "time_to_display": self.time_to_display,
            "members_dict": self.member_dict,
            "members_count": self.members_count
        }
        # Find dir 'saves'. If not - create
        for file in os.listdir(path='.'):
            if file == 'saves':
                break
        else:
            os.mkdir('saves')
        # Save raid in txt file
        file_name = f"saves/{self.captain_name}_{'-'.join(self.time_leaving.split(':'))}.json"
        with open(file_name, 'w', encoding='utf-8') as save_file:
            json.dump(raid_information, save_file)


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
        self.title = f"{self.raid.captain_name} {self.raid.server} {self.raid.time_leaving}"
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

        self.table_path = os.path.join('images', 'raid_') + str(self.raid.time_leaving) + ".png"
        cv2.imwrite(self.table_path, img)

    def create_text_table(self):
        table = self.title
        for name in self.raid.member_dict:
            table += f"{name}\n"
        return table

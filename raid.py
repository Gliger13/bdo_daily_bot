import datetime
import random
import os

import cv2
import numpy as np
import instruments
from datetime import datetime, timedelta
from PIL import ImageFont, ImageDraw, Image


class Raid:
    """
    Create Raid Object that contain members amount of members and etc

    """
    def __init__(self, captain_name, server, time_leaving, time_reservation_open, reservation_count=0):
        self.captain_name = captain_name
        self.server = server
        self.time_leaving = time_leaving
        self.time_reservation_open = time_reservation_open
        self.reservation_count = int(reservation_count) + 2
        self.title = f"{self.captain_name} {self.server} {self.time_leaving}"
        self.member_dict = {}
        self.member_count = 0
        self.members = self.member_count + self.reservation_count
        self.places_left = 20 - self.members
        current_time = datetime.now()
        self.time_of_creation = str(current_time.hour) + '_' + str(current_time.minute) + '_' + str(current_time.second)
        self.image_link = None
        self.collection_msg = None
        self.guild = None
        self.table_msg = None
        self.info_msg = None
        self.time_to_display = []
        self.is_delete_raid = False
        self.task_list = []

    def __iadd__(self, name_new_member):
        if self.places_left == 0:
            return False
        self.member_count += 1
        self.members = self.member_count + self.reservation_count
        self.places_left = 20 - self.members
        self.member_dict.update({name_new_member: self.member_count})
        return self

    def __isub__(self, name_remove_member):
        if self.member_dict.get(name_remove_member):
            del self.member_dict[name_remove_member]
            self.member_count -= 1
            self.members = self.member_count + self.reservation_count
            self.places_left = 20 - self.members
            return self
        else:
            return False

    def __cmp__(self, other):
        if self.members > other.members:
            return 1
        elif self.members == other.members:
            return 0
        else:
            return -1

    def __lt__(self, other):
        return self.members < other.members

    def __gt__(self, other):
        return self.members > other.members

    def update_info(self):
        self.members = self.member_count + self.reservation_count
        self.places_left = 20 - self.members

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
            hh_mm = f'{hh}:{mm}' if mm > 10 else f'{hh}:0{mm}'
            self.time_to_display.append((sec, hh_mm))
        return self.time_to_display

    def save_raid(self):
        # Find dir 'saves'. If not - create
        for file in os.listdir(path='.'):
            if file == 'saves':
                break
        else:
            os.mkdir('./saves')
        # Save raid in txt file
        file_name = f"./saves/{self.captain_name}_{'-'.join(self.time_leaving.split(':'))}.txt"
        with open(file_name, 'w') as save_file:
            save_file.write(f'{self.captain_name},{self.server},{self.time_leaving},'
                            f'{self.time_reservation_open},{self.reservation_count}\n')
            for name in self.member_dict:
                save_file.write(name + ' ')

    def create_table(self):
        # Create a black image
        max_high = 420
        max_widht = 200
        columns = 21
        line_width = 1
        color_title = (random.randrange(30, 230), random.randrange(30, 230), random.randrange(30, 230))
        # Create white image
        img = np.zeros((max_high, max_widht, 3), np.uint8)
        img[::, ::] = 255
        # Draw reservation red space
        cv2.rectangle(img, (0, max_high), (max_widht, max_high - max_high // columns * self.reservation_count),
                      (0, 0, 255), -1)
        # Draw lines of table
        for i in range(21):
            # Set bottom left and top right coordinate of 21 rectangles
            point_one = 0, (max_high // columns) * (i + 1)
            point_two = max_widht - line_width // 2, (max_high // columns) * i
            # Set coordinate of numerations
            point_number = 2, (max_high // columns) * (i + 1) - 4
            # Draw 21 rectangles
            cv2.rectangle(img, point_one, point_two, (0, 0, 0), line_width)
            if i > 0:  # Draw numeration of 20 columns
                cv2.putText(img, str(i), point_number, cv2.FONT_HERSHEY_DUPLEX, 0.5, (10, 10, 10), 1, cv2.LINE_AA)
        # Draw vertical line... Yes its rectangle, not line but line
        cv2.rectangle(img, (0, max_high - line_width // 2), (30, 0), (0, 0, 0), line_width)
        # Create random color block in top title
        cv2.rectangle(img, (0, max_high // columns), (max_widht, 0), color_title, -1)
        # Draw text
        fontpath = "./cambria.ttc"  # Choose font in window local storage
        font = ImageFont.truetype(fontpath, 18, encoding="UTF-8")  # Set size and encoding
        img_pil = Image.fromarray(img)  # Change type to work with Pillow
        draw = ImageDraw.Draw(img_pil)
        i = 0
        for name in self.member_dict:
            point_name = 35, (max_high // columns * (i + 1))  # Set coordinate of text message
            draw.text(point_name, name, font=font, fill=(0, 0, 0, 0))
            i += 1
        # Draw name of captain in title
        draw.text((5, 0), self.title, font=font, fill=(0, 0, 0, 0))
        img = np.array(img_pil)  # Changing type back into NumPy array

        # Save image on local storage
        # Find dir 'images'. If not - create
        for file in os.listdir(path='.'):
            if file == 'images':
                break
        else:
            os.mkdir('./images')
        image_link = "./images/raid_" + str(self.time_of_creation) + ".png"
        cv2.imwrite(image_link, img)
        self.image_link = image_link
        return self.image_link


if __name__ == "__main__":
    my_raid = Raid("Captain", "K-1", "0:15", "14:50", 3)



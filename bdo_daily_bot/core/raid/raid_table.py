"""
Contain class for producing raid table image
"""
import os
import random

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from bdo_daily_bot.settings.settings import BOT_DATA_PATH


class RaidTable:
    """
    Class for producing raid table images
    """
    # Text settings

    # Size
    HEIGHT = 420

    # For text
    TEXT_FONT_SIZE = 18  # pt
    # Font path
    ROOT_DIR = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    FONT_PATH = os.path.join(ROOT_DIR, "settings", "font_table.ttf")
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

    def __init__(self, raid):
        self.raid = raid
        self.old_member_dict = self.raid.members.copy()
        self.old_reservation_count = self.raid.reservation_count
        self.title = f"{self.raid.captain.nickname} {self.raid.bdo_server} {self.raid.time.normal_time_leaving}"
        self.table_path = None

    def get_width(self):
        title_width = RaidTable.FONT.getsize(self.title)[0]
        if self.raid.members:
            max_name = max([member.nickname for member in self.raid.members])
            max_name_row_width = RaidTable.NUMBER_SIZE_WIDTH + RaidTable.FONT.getsize(max_name)[0]
            # 15 - 15px - offset the indent
            return max(title_width, max_name_row_width) + 15
        # 15 - 15px - offset the indent
        return title_width + 15

    def create_table(self):
        width = self.get_width()
        # Build frame of table
        # Create white image
        img = np.zeros((RaidTable.HEIGHT, width, 3), np.uint8)
        img[::, ::] = 255

        # Draw reservation red space
        start_point = (0, RaidTable.HEIGHT)
        end_point = (width, RaidTable.HEIGHT - RaidTable.HEIGHT // RaidTable.COLUMNS * self.raid.reservation_count)
        color = (0, 0, 255)
        rect_thickness = -1  # Thickness of -1 px will fill the rectangle shape by the specified color
        cv2.rectangle(img, start_point, end_point, color, rect_thickness)

        # Draw lines of table
        for number in range(21):
            # Set bottom left and top right coordinate of 21 rectangles
            start_point = 0, (RaidTable.HEIGHT // RaidTable.COLUMNS) * (number + 1)
            end_point = width - RaidTable.LINE_WIDTH // 2, (RaidTable.HEIGHT // RaidTable.COLUMNS) * number
            # Set coordinate of numerations
            point_number = 2, (RaidTable.HEIGHT // RaidTable.COLUMNS) * (number + 1) - 4
            # Draw 21 rectangles
            cv2.rectangle(img, start_point, end_point, (0, 0, 0), RaidTable.LINE_WIDTH)
            if number > 0:  # Draw numeration of 20 columns
                cv2.putText(
                    img=img,
                    text=str(number),
                    org=point_number,
                    fontFace=RaidTable.NUMBER_FONT_FACE,
                    fontScale=RaidTable.NUMBER_FONT_SCALE,
                    color=RaidTable.NUMBER_COLOR,
                    thickness=RaidTable.NUMBER_THICKNESS,
                    lineType=RaidTable.NUMBER_BASE_LINE,
                )

        # Draw vertical line... Yes its rectangle, not line but line
        start_point = (0, RaidTable.HEIGHT)
        end_point = (30, 0)
        color = (0, 0, 0)
        rect_thickness = 1
        cv2.rectangle(img, start_point, end_point, color, rect_thickness)

        # Create random color block in top title
        start_point = (0, RaidTable.HEIGHT // RaidTable.COLUMNS)
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
        members_nicknames = [member.nickname for member in self.raid.members]
        for name in members_nicknames:
            # Set coordinate of text message
            point_name = 35, (RaidTable.HEIGHT // RaidTable.COLUMNS * (name_number + 1))
            draw.text(point_name, name, font=RaidTable.FONT, fill=(0, 0, 0, 0))
            name_number += 1

        # Draw name of captain in title
        draw.text((5, 0), self.title, font=RaidTable.FONT, fill=(0, 0, 0, 0))

        # Changing type back into NumPy array
        img = np.array(img_pil)

        self._save(img)
        return self.table_path

    def update_table(self, raid):
        if not self.old_member_dict == raid.members or not self.old_reservation_count == raid.reservation_count:
            self.__init__(raid)
            self.old_member_dict = raid.members.copy()
            self.old_reservation_count = raid.reservation_count
            self.create_table()
        else:
            return

    def _save(self, img):
        # Save image on local storage
        # Find dir 'images'. If not - create
        self.table_path = os.path.join(BOT_DATA_PATH, 'images')
        if not os.path.isdir(self.table_path):
            os.mkdir(self.table_path)

        file_name = self.raid.captain.nickname + '_' + str(self.raid.time.kebab_time_leaving) + ".png"
        self.table_path = os.path.join(self.table_path, file_name)
        cv2.imwrite(self.table_path, img)

    def create_text_table(self):
        table = f"{self.title}\n"
        members_nicknames = [member.nickname for member in self.raid.members]
        for name in members_nicknames:
            table += f"**{name}**\n"
        return table

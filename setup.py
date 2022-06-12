"""Setup bdo daily bot"""
from os.path import dirname, join

from setuptools import find_packages, setup

# Package metadata

PACKAGE_NAME = "bdo_daily_bot"
VERSION = "v3.1.3"
AUTHOR = "Andrei Zaneuski"
AUTHOR_EMAIL = "zanevskiyandrey@gmail.com"
DESCRIPTION = "Discord Bot to organize and collect daily sea raids in the game Black Desert Online[RU] (BDO)"
URL = "https://github.com/Gliger13/bdo_daily_bot"

with open(join(dirname(__file__), 'README.md'), encoding="utf-8") as readme_file:
    LONG_DESCRIPTION = readme_file.read()

with open(join(dirname(__file__), "LICENSE"), encoding="utf-8") as license_file:
    LICENSE = license_file.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    packages=find_packages(),
    package_dir={'bdo_daily_bot': 'bdo_daily_bot'},
    scripts=[join("bdo_daily_bot", "bot.py")]
)

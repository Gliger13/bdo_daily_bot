"""Setup bdo daily bot"""
from os.path import dirname, join

from setuptools import find_packages, setup

# Package metadata

PACKAGE_NAME = "bdo_daily_bot"
VERSION = "v3.1.4"
AUTHOR = "Andrei Zaneuski"
AUTHOR_EMAIL = "zanevskiyandrey@gmail.com"
DESCRIPTION = "Discord Bot to organize and collect daily sea raids in the game Black Desert Online[RU] (BDO)"
URL = "https://github.com/Gliger13/bdo_daily_bot"
CLASSIFIERS = [
    "Programming Language :: Python :: 3.10",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Development Status :: 5 - Production/Stable",
    "Framework :: AsyncIO",
]

with open(join(dirname(__file__), 'README.md'), encoding="utf-8") as readme_file:
    LONG_DESCRIPTION = readme_file.read()

LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"

with open(join(dirname(__file__), "LICENSE"), encoding="utf-8") as license_file:
    LICENSE = license_file.read()

TESTS_REQUIREMENTS = [
    "pytest",
    "pytest-asyncio",
    "pytest-cov",
    "selenium",
    "tabulate",
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    url=URL,
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    package_dir={'bdo_daily_bot': 'bot'},
    python_requires=">=3.10",
    extras_require={
        "testing": TESTS_REQUIREMENTS
    },
    entry_points={"console_scripts": [
        "run_bdo_daily_bot = bot.bot",
    ]},
)

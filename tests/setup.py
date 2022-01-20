"""
Setup of test framework to test bdo daily bot
"""
from os.path import dirname, join

from setuptools import find_packages, setup

setup(
    name='DiscordBotBDO',
    version='0.0.1',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
)

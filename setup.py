"""
Setup bdo daily bot and it's depending packages
"""
from os.path import dirname, join

from setuptools import find_packages, setup

setup(
    name='DiscordBotBDO',
    version='3.0.0_unstable',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
)

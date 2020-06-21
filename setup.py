from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='DiscordBotBDO',
    version='2.0.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
)


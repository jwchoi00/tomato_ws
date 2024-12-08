from setuptools import find_packages
from setuptools import setup

setup(
    name='tomato_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('tomato_interfaces', 'tomato_interfaces.*')),
)

from setuptools import find_packages
from setuptools import setup

setup(
    name='project2_interfaces',
    version='0.1.0',
    packages=find_packages(
        include=('project2_interfaces', 'project2_interfaces.*')),
)

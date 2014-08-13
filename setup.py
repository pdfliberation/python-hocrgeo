#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding

import hocrgeo

setup(
    name='hocrgeo',
    version=hocrgeo.__version__,
    description='Python tool for converting hOCR files to geographic file formats',
    author='Daniel Cloud',
    author_email='daniel@danielcloud.org',
    license = hocrgeo.__license__,
    url='https://github.com/pdfliberation/python-hocrgeo',
    install_requires=['Shapely', 'lxml', 'beautifulsoup4'],
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)
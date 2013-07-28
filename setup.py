#!/usr/bin/env python

from setuptools import setup

setup(
    name='rtorrent-automover',
    version='2.2.0',
    description='Automover ', 
    author='John Doee',
    maintainer='John Doee',
    url='https://github.com/johndoee/',
    packages=['automover', 'automover.clients', 'automover.sections'],
    install_requires=['tendo'],
    license='BSD-new',
    entry_points={ 'console_scripts': [
        'automover = automover.cmd:commandline_handler',
    ]},
)

#!/usr/bin/env python

from setuptools import setup

def read_description():
    import os
    path = os.path.join(os.path.dirname(__file__), 'README.rst')
    try:
        with open(path) as f:
            return f.read()
    except:
        return 'No description found'

setup(
    name='rtorrent-automover',
    version='2.3.1',
    description='Automoving torrents.',
    long_description=read_description(),
    author='Anders Jensen',
    author_email='johndoee+autotorrent@tidalstream.org',
    maintainer='Anders Jensen',
    url='https://github.com/johndoee/',
    packages=['automover', 'automover.clients', 'automover.sections'],
    install_requires=['tendo'],
    license='BSD-new',
    entry_points={ 'console_scripts': [
        'automover = automover.cmd:commandline_handler',
    ]},
)

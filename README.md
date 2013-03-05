rtorrent-automover
==================

Moves complete torrents automagically for rtorrent.
Can also cleanup when something is both moved and seeded enough.

Instructions
------------

How to get this ship sailing.
First, rtorrent needs to download stuff to specific folders, as that's how we figure out where to move from.

Second, XMLRPC needs to be configured, see the rutorrent project for instructions: http://code.google.com/p/rutorrent/wiki/Installation


### Installation
    virtualenv automover
    cd automover
    bin/pip install git+git://github.com/JohnDoee/rtorrent-automover.git

### Configuration
There is an example config file, modify it for your needs (https://github.com/JohnDoee/rtorrent-automover/blob/master/automover.conf.example).

```automove_syntax``` is an optional option that can help sort e.g. tv show. The example used, ```%(show)s/Season.%(season)0.2i/``` will try to sort tv shows by show name and season.

### Execute

```bin/automover automover.conf``` and it will try to move stuff.
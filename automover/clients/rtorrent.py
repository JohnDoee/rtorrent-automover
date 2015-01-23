from __future__ import division

import httplib
import os
import time

from datetime import datetime
from xmlrpclib import ServerProxy, Transport

from automover.client import Client, Torrent

TIMEOUT = 60*5

class TimeoutTransport(Transport):
    def make_connection(self, host):
        #return an existing connection if possible.  This allows
        #HTTP/1.1 keep-alive.
        if self._connection and host == self._connection[0]:
            return self._connection[1]

        # create a HTTP connection object from a host descriptor
        chost, self._extra_headers, x509 = self.get_host_info(host)
        #store the host argument along with the connection object
        self._connection = host, httplib.HTTPConnection(chost, timeout=TIMEOUT)
        return self._connection[1]


class RTorrentClient(Client):
    name = 'rtorrent'

    def __init__(self, xmlrpc_url):
        self.proxy = ServerProxy(xmlrpc_url, transport=TimeoutTransport())

    def list(self):
        torrents = []
        query = self.proxy.d.multicall(['main', 'd.get_hash=', 'd.name=', 'd.timestamp.finished=', 'd.get_ratio=', 'd.get_complete=', 'd.directory=', 'd.is_multi_file='])
        for torrent_hash, name, finish_time, ratio, is_complete, path, is_multi_file in query:
            finish_time = datetime.fromtimestamp(finish_time)
            ratio = ratio / 1000

            if not is_multi_file:
                path = os.path.join(path, name)

            torrents.append(Torrent(self, torrent_hash, finish_time, ratio, path, is_complete))

        infohashes = [x[0] for x in query]
        trackers = [x[0] for x in self.proxy.system.multicall([{'methodName': 't.multicall', 'params': [infohash, '', ['t.get_url=']]} for infohash in infohashes])]

        for torrent, tracker in zip(torrents, trackers):
            setattr(torrent, '_trackers', [x[0] for x in tracker])

        return torrents

    def delete(self, torrent):
        self.proxy.d.erase(torrent.torrent_id)
        return True

    def stop(self, torrent):
        self.proxy.d.stop(torrent.torrent_id)

        i = 0
        while self._get_state(torrent) != 0 and i < 10:
            time.sleep(0.5)
            i += 1

        return i != 10

    def start(self, torrent):
        self.proxy.d.start(torrent.torrent_id)

        i = 0
        while self._get_state(torrent) != 1 and i < 10:
            time.sleep(0.5)
            i += 1

        return i != 10

    def set_path(self, torrent, path):
        self.proxy.d.set_directory(torrent.torrent_id, path)
        return True

    def trackers(self, torrent):
        return torrent._trackers

    def _get_state(self, torrent):
        return self.proxy.d.state(torrent.torrent_id)

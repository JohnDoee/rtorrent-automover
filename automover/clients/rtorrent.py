from __future__ import division

import os
import time
from datetime import datetime
from xmlrpclib import ServerProxy

from automover.client import Client, Torrent

class RTorrentClient(Client):
    name = 'rtorrent'
    
    def __init__(self, xmlrpc_url):
        self.proxy = ServerProxy(xmlrpc_url)
    
    def list(self):
        torrents = []
        for torrent_hash in self.proxy.download_list():
            finish_time = datetime.fromtimestamp(self.proxy.d.timestamp.finished(torrent_hash))
            ratio = self.proxy.d.get_ratio(torrent_hash) / 1000
            is_complete = self.proxy.d.get_complete(torrent_hash)
            
            path = self.proxy.d.directory(torrent_hash)
            if not self.proxy.d.is_multi_file(torrent_hash):
                path = os.path.join(path, self.proxy.d.name(torrent_hash))
            
            torrents.append(Torrent(self, torrent_hash, finish_time, ratio, path, is_complete))
        
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
        return [self.proxy.t.get_url('%s:t%s' % (torrent.torrent_id, i)) for i in range(self.proxy.d.get_tracker_size(torrent.torrent_id))]
    
    def _get_state(self, torrent):
        return self.proxy.d.state(torrent.torrent_id)
    
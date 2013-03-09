from copy import copy

from automover.section import Automover
from automover.client import Client, Torrent

__all__ = [
    'DummyAutomover',
    'DummyClient',
    'DummyTorrent',
]

class DummyTorrent(Torrent):
    def __init__(self, client, torrent_id, finish_time, ratio, path, is_complete, running, trackers):
        self.running = running
        self._trackers = trackers
        super(DummyTorrent, self).__init__(client, torrent_id, finish_time, ratio, path, is_complete)
    
    def _move(self, path, destination_path):
        self.latest_move = (path, destination_path)
    
    def trackers(self):
        return self._trackers
    

class DummyClient(Client):
    def __init__(self):
        self.torrents = []
    
    def list(self):
        return copy(self.torrents)
    
    def delete(self, torrent):
        self.torrents.remove(torrent)
        return True
    
    def stop(self, torrent):
        torrent.running = False
        return True
    
    def start(self, torrent):
        torrent.running = True
        return True
    
    def set_path(self, torrent, path):
        torrent.path = path
    
    def trackers(self, torrent):
        return torrent.trackers


class DummyAutomover(Automover):
    name = 'dummy'
    
    def __init__(self, source_paths, destination_paths, automove_syntax, test_mode=False):
        super(DummyAutomover, self).__init__(source_paths, destination_paths, automove_syntax, test_mode=False)
        self._free_spaces = {}
    
    def get_free_space(self, p):
        return ([y for x, y in self._free_spaces.items() if p.startswith(x)] + [0])[0]
    
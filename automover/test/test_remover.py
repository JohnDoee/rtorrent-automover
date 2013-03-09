import unittest
from datetime import datetime, timedelta

from automover.test.helpers import *

from automover.remover import handle_remove

class TestRemover(unittest.TestCase):
    def setUp(self):
        self.client = client = DummyClient()
        self.torrents = [
            DummyTorrent(client, '1', datetime.now(), 0, '/matchpath/', False, True, ['http://matchtracker.com']),
            DummyTorrent(client, '2', datetime.now(), 2, '/matchpath/', True, True, ['http://matchtracker.com']),
            DummyTorrent(client, '3', datetime.now()-timedelta(hours=20), 0.5, '/matchpath/', True, True, ['http://matchtracker.com']),
            DummyTorrent(client, '4', datetime.now()-timedelta(hours=50), 50, '/matchpath/', True, True, ['http://matchtracker.com']),
            DummyTorrent(client, '5', datetime.now()-timedelta(hours=50), 50, '/matchpath/', True, True, ['http://matchtracker.com']),
            DummyTorrent(client, '6', datetime.now(), 50, '/matchpath/', False, True, ['http://matchtracker.com']),
            DummyTorrent(client, '7', datetime.now(), 50, '/matchpath/', True, True, ['http://matchNOTtracker.com']),
            DummyTorrent(client, '8', datetime.now(), 50, '/matchNOTpath/', True, True, ['http://matchtracker.com']),
        ]
        self.client.torrents = self.torrents
    
    def test_timed_remove(self):
        handle_remove(self.client, {'fakesite1': ('time', 'matchtracker', '3')}, ['/matchpath'])
        self.assertEqual([torrent.torrent_id for torrent in self.torrents], ['1', '2', '6', '7', '8'], 'Did not remove correct torrents')
    
    def test_ratio_remove(self):
        handle_remove(self.client, {'fakesite1': ('ratio', 'matchtracker', 1.5)}, ['/matchpath'])
        self.assertEqual([torrent.torrent_id for torrent in self.torrents], ['1', '3', '6', '7', '8'], 'Did not remove correct torrents')
    
    def test_combined_remove(self):
        handle_remove(self.client, {'fakesite1': ('ratio', 'matchtracker', 1.5), 'fakesite2': ('time', 'matchtracker', '3')}, ['/matchpath'])
        self.assertEqual([torrent.torrent_id for torrent in self.torrents], ['1', '6', '7', '8'], 'Did not remove correct torrents')
#import os
#import shutil
#import unittest
#import tempfile
#from datetime import datetime
#
#from automover.test.helpers import *
#
#
#class TestSection(unittest.TestCase):
#    def setUp(self):
#        self.source_dir_1 = tempfile.mkdtemp()
#        self.source_dir_2 = tempfile.mkdtemp()
#        self.destination_dir_1 = tempfile.mkdtemp()
#        self.destination_dir_2 = tempfile.mkdtemp()
#        #source_paths, destination_paths, automove_syntax, test_mode=False
#        self.automover = DummyAutomover([self.source_dir_1, self.source_dir_2], [self.destination_dir_1, self.destination_dir_2], None)
#        self.automover._free_spaces[self.source_dir_1] = 1000000000
#        self.automover._free_spaces[self.source_dir_2] = 200000
#        self.automover_syntax = DummySyntax([self.source_dir_1, self.source_dir_2], [self.destination_dir_1, self.destination_dir_2], '%(testvar)s/')
#        self.automover_syntax._free_spaces = self.automover._free_spaces
#        
#        self.automover_syntax.get_interpolation_variables = lambda x, y:'name'
#        self.client = DummyClient()
#        
#        p1 = os.path.join(self.source_dir_1, 'folder1')
#        p2 = os.path.join(self.source_dir_2, 'folder1')
#        p3 = os.path.join(self.destination_dir_1, 'folder1')
#        p4 = os.path.join(self.destination_dir_2, 'folder1')
#        f5 = os.path.join(self.destination_dir_2, 'file1')
#        f5 = os.path.join(self.source_dir_1, 'file1')
#        self.torrents = [
#            DummyTorrent(client, '1', datetime.now(), 0, '/matchpath/', False, True, []),
#            DummyTorrent(client, '2', datetime.now(), 0, '/matchpath/', True, True, []),
#            DummyTorrent(client, '3', datetime.now(), 0, '/matchpath/', True, True, []),
#            DummyTorrent(client, '4', datetime.now(), 0, '/matchpath/', True, True, []),
#            DummyTorrent(client, '5', datetime.now(), 0, '/matchpath/', True, True, []),
#            DummyTorrent(client, '6', datetime.now(), 0, '/matchpath/', False, True, []),
#            DummyTorrent(client, '7', datetime.now(), 0, '/matchpath/', True, True, []),
#            DummyTorrent(client, '8', datetime.now(), 0, '/matchNOTpath/', True, True, []),
#        ]
#    
#    def tearDown(self):
#        shutil.rmtree(self.source_dir_1)
#        shutil.rmtree(self.source_dir_2)
#        shutil.rmtree(self.destination_dir_1)
#        shutil.rmtree(self.destination_dir_2)
#    
#    def _create_file(self, path, size):
#        with open(path, 'wb') as f:
#            f.write('-'*size)
#    
#    def test_move(self):
#        self.automover_syntax
#    
#    
#    
import os
import shutil
import unittest
import tempfile

from automover.utils import get_size

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def _create_file(self, path, size):
        with open(path, 'wb') as f:
            f.write('-'*size)
    
    def test_get_size(self):
        f1 = os.path.join(self.temp_dir, 'f1')
        f2 = os.path.join(self.temp_dir, 'f2')
        d1 = os.path.join(self.temp_dir, 'tempfolder')
        os.mkdir(d1)
        f3 = os.path.join(d1, 'f3')
        
        self._create_file(f1, 10)
        self._create_file(f2, 10)
        self._create_file(f3, 10)
        
        self.assertEqual(get_size(f1), 10, 'One file created not correct size')
        self.assertEqual(get_size(self.temp_dir), 30, 'Folder size not correct')
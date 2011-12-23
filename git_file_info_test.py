import unittest
import os
from git_file_info import *

class TestGitFileInfo(unittest.TestCase):

    def setUp(self):
      self.dir       = os.path.join("tmp", "testing")
      self.test_file = os.path.join(self.dir, "foo.txt")
      os.makedirs(self.dir)
      open(self.test_file, 'w').close()

    def test_path(self):
      file_info = GitFileInfo(os.path.realpath(self.test_file))
      self.assertEqual(self.test_file, file_info.path())

    def test_remote_repository(self):
      file_info = GitFileInfo(os.path.realpath(self.test_file))
      self.assertEqual("git@github.com:noahd1/SublimeCodeClimate.git", file_info.remote_repository())

    def tearDown(self):
      os.remove(self.test_file)
      os.removedirs(self.dir)

if __name__ == '__main__':
    unittest.main()

import unittest
import os
import subprocess
import shutil
import git_utils

class TestGitFileInfo(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    remote_repo = os.path.join("/", "tmp", "fake_remote_repo")
    os.makedirs(remote_repo)
    os.chdir(remote_repo)
    subprocess.call(["git", "init"])
    git_folders = os.path.join(remote_repo, "doc", "testing")
    os.makedirs(git_folders)
    git_file = os.path.join(git_folders, "README.txt")
    open(git_file, 'w').close()
    subprocess.call(["git", "add", "."])
    subprocess.call(["git", "commit", "-m", "initial commit"])
    os.chdir("/tmp")
    subprocess.call(["git", "clone", remote_repo, "fake_local_copy"])
    os.mkdir("/tmp/not_git_repo")

  def test_remote_repository(self):
    file_info = git_utils.GitFileInfo("/tmp/fake_local_copy/doc/testing/README.txt")
    self.assertEqual("/tmp/fake_remote_repo", file_info.remote_repository())

  def test_remote_repository_raises_error(self):
    file_info = git_utils.GitFileInfo("/tmp/not_git_repo")
    self.assertRaises(git_utils.GitInfoError, file_info.remote_repository)

  def test_path(self):
    file_info = git_utils.GitFileInfo("/tmp/fake_local_copy/doc/testing/README.txt")
    self.assertEqual("doc/testing/README.txt", file_info.path())

  def test_not_path(self):
    file_info = git_utils.GitFileInfo("/tmp/not_git_repo")
    self.assertRaises(git_utils.GitInfoError, file_info.path)

  def test_git_root(self):
    file_info = git_utils.GitFileInfo("/tmp/fake_local_copy/doc/testing/README.txt")
    self.assertEqual("/tmp/fake_local_copy", file_info.git_root())

  def test_git_root_none(self):
    file_info = git_utils.GitFileInfo("/tmp/not_git_repo")
    self.assertEqual(None, file_info.git_root())

  @classmethod
  def tearDownClass(cls):
    shutil.rmtree("/tmp/fake_remote_repo")
    shutil.rmtree("/tmp/fake_local_copy")
    shutil.rmtree("/tmp/not_git_repo")

if __name__ == '__main__':
    unittest.main()

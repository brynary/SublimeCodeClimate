import subprocess
import os

class GitFileInfo:

  def __init__(self, full_file_path):
    self.full_file_path = full_file_path

  def remote_repository(self):
    folder_name = os.path.split(self.full_file_path)[0]
    git_command = ["git", "config", "--get", "remote.origin.url"]
    original_cwd = os.getcwd()
    os.chdir(folder_name)
    popen = subprocess.Popen(git_command, stdout = subprocess.PIPE)
    repo = popen.communicate()[0].strip()
    if repo == "":
      raise GitInfoError(self.full_file_path + " does not appear to be part of a git repo")
    os.chdir(original_cwd)
    return repo

  def _git_root(self, path):
    if os.path.isfile(path):
      test_dir = os.path.split(path)[0]
    else:
      test_dir = path

    if os.path.exists(os.path.join(test_dir, ".git")):
      return test_dir
    elif os.path.split(path)[1] == '': # reached file system root
      return None
    else:
      parent = os.path.split(path)[0]
      return self._git_root(parent)

  def path(self):
    git_root = self._git_root(self.full_file_path)
    if git_root == None:
      raise GitInfoError(self.full_file_path + " does not appear to be part of a git repo")
    else:
      return self.full_file_path[len(git_root) + 1:]

class GitInfoError(Exception):
  pass


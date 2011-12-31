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

  def path(self):
    if self.git_root() == None:
      raise GitInfoError(self.full_file_path + " does not appear to be part of a git repo")
    else:
      return self.full_file_path[len(self.git_root()) + 1:]

  def git_root(self):
    return self._git_root(os.path.split(self.full_file_path)[0])

  def _git_root(self, path):
    head, tail = os.path.split(path)
    if os.path.exists(os.path.join(path, ".git")):
      return path
    elif tail == '': # reached file system root
      return None
    else:
      return self._git_root(head)

class GitInfoError(Exception):
  pass


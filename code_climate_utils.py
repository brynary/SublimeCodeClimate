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
    path = []
    parent_dir, base = os.path.split(self.full_file_path)
    path.insert(0, base)
    while not(self.is_git_root(parent_dir)):
      parent_dir, base = os.path.split(parent_dir)
      path.insert(0, base)
    return os.path.join(*path)

  def is_git_root(self, dir):
    return os.path.exists(os.path.join(dir, ".git"))

class GitInfoError(Exception):
  pass


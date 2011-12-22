import os
import subprocess
import webbrowser
import sublime, sublime_plugin

def git_root(directory):
  while directory:
    if os.path.exists(os.path.join(directory, '.git')):
      return directory
    parent = os.path.realpath(os.path.join(directory, os.path.pardir))
    if parent == directory:
      # /.. == /
      return False
    directory = parent
  return False

def get_repository_path(full_name):
  folder_name, file_name = os.path.split(full_name)
  return full_name.replace(git_root(folder_name) + "/", '')

def get_remote_repository(full_name):
  folder_name, file_name = os.path.split(full_name)

  git_command = ["git", "config", "--get", "remote.origin.url"]
  os.chdir(folder_name)
  popen = subprocess.Popen(git_command, stdout = subprocess.PIPE)
  return popen.communicate()[0].strip()

class CodeClimateCommand(sublime_plugin.TextCommand):

  def run(self, args):
    file_name = self.view.file_name()
    url = "https://codeclimate.com/browse?repo=" + get_remote_repository(file_name) + "&path=" + get_repository_path(file_name)
    print "Opening URL: " + url
    webbrowser.open_new(url)

import os
import sys
import urllib
import webbrowser
import sublime, sublime_plugin
import git_utils

class CodeClimateCommand(sublime_plugin.TextCommand):

  def run(self, args):
    try:
      file_info = git_utils.GitFileInfo(self.view.file_name())
      params = urllib.urlencode({"repo": file_info.remote_repository(), "path": file_info.path()})
      url = "https://codeclimate.com/browse?%s" % params
      print "Opening URL: " + url
      webbrowser.open_new(url)
    except git_utils.GitInfoError as err:
      sys.stderr.write("Cannot open file in CodeClimate: " + str(err))

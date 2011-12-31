import os
import urllib
import webbrowser
import git_utils
import sublime, sublime_plugin

class CodeClimateCommand(sublime_plugin.TextCommand):

  def run(self, args):
    file_info = git_utils.GitFileInfo(self.view.file_name())
    params = urllib.urlencode({"repo": file_info.remote_repository(), "path": file_info.path()})
    url = "https://codeclimate.com/browse?%s" % params
    print "Opening URL: " + url
    webbrowser.open_new(url)

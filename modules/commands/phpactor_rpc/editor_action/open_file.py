import sublime
import sublime_plugin
from ....utils import *

class PhpactorEditorActionOpenFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, force_reload, path, offset, target):
        # navigate command returns relative path for some reason
        if path.find('/') != 0:
            path = find_working_dir(self.view) + '/' + path

        self.view.run_command('tk_open_file_at_offset', { 'file_path': path, 'offset': offset } )
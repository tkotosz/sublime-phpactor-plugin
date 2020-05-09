import sublime_plugin
import sublime
from ...utils import *
from ...settings import *

class PhpactorSidebarCopyRelativePathCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        file_absolute_path = files[0]
        file_relative_path = file_absolute_path.replace(find_working_dir(self.window, file_absolute_path) + '/', '')
        sublime.set_clipboard(file_relative_path)

    def is_visible(self, files):
        return len(files) == 1 and get_sidebar_menu_setting('copy_relative_path', 'enabled', False)
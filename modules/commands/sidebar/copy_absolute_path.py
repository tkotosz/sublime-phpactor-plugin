import sublime_plugin
import sublime
from ...settings import *

class PhpactorSidebarCopyAbsolutePathCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        sublime.set_clipboard(files[0])

    def is_visible(self, files):
        return len(files) == 1 and get_sidebar_menu_setting('copy_absolute_path', 'enabled', False)
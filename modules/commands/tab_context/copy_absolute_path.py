import sublime_plugin
import sublime
from ...settings import *

class PhpactorTabContextCopyAbsolutePathCommand(sublime_plugin.WindowCommand):
    def run(self, group, index):
        view = self.window.views_in_group(group)[index]
        sublime.set_clipboard(view.file_name())

    def is_visible(self):
        return get_tab_context_menu_setting('copy_absolute_path', 'enabled', False)

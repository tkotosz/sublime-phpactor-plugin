import sublime_plugin
import sublime
from ...settings import *

class PhpactorContextCopyAbsolutePathCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        sublime.set_clipboard(view.file_name())

    def is_visible(self):
        return get_context_menu_setting('copy_absolute_path', 'enabled', False)

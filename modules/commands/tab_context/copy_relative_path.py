import sublime_plugin
import sublime
from ...utils import *
from ...settings import *

class PhpactorTabContextCopyRelativePathCommand(sublime_plugin.WindowCommand):
    def run(self, group, index):
        view = self.window.views_in_group(group)[index]
        file_absolute_path = view.file_name()
        file_relative_path = file_absolute_path.replace(find_working_dir(self.window, file_absolute_path) + '/', '')
        sublime.set_clipboard(file_relative_path)

    def is_visible(self):
        return get_tab_context_menu_setting('copy_relative_path', 'enabled', False)

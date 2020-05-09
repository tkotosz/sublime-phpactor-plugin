import sublime_plugin
import sublime
from ...settings import *

class PhpactorTabContextRevealInSideBarCommand(sublime_plugin.WindowCommand):
    def run(self, group, index):
        view = self.window.views_in_group(group)[index]
        self.window.focus_view(view)
        self.window.run_command('reveal_in_side_bar')

    def is_visible(self):
        return get_tab_context_menu_setting('reveal_in_side_bar', 'enabled', False)

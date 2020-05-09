import sublime_plugin
from ...settings import *

class PhpactorSidebarClassNewCommand(sublime_plugin.WindowCommand):
    def run(self, dirs):
        request = {
            'action': 'class_new',
            'parameters': {
                'current_path': dirs[0] + '/'
            }
        }
        self.window.active_view().run_command('phpactor_rpc', request)

    def is_visible(self, dirs):
        return len(dirs) == 1 and get_sidebar_menu_setting('new_php_class', 'enabled', False)
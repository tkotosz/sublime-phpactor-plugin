import sublime_plugin
from ...settings import *

class PhpactorSidebarCopyClassCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        request = {
            'action': 'copy_class',
            'parameters': {
                'source_path': files[0]
            }
        }
        self.window.active_view().run_command('phpactor_rpc', request)

    def is_visible(self, files):
        return len(files) == 1 and files[0].rsplit('.', 1)[-1] == 'php' and get_sidebar_menu_setting('copy_php_class', 'enabled', False)
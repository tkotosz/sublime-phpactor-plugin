import sublime_plugin

from ...settings import *

class PhpactorReferencesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'references',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset',
                'filesystem': get_command_setting('references', 'filesystem', 'git')
            }
        }
        self.view.run_command('phpactor_rpc', request)
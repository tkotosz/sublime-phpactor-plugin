import sublime_plugin

class PhpactorReferencesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'references',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset'
                #'filesystem': 'composer'
            }
        }
        self.view.run_command('phpactor_rpc', request)
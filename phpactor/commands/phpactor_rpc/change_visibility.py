import sublime_plugin

class PhpactorChangeVisibilityCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'change_visibility',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset'
            }
        }

        self.view.run_command('phpactor_rpc', request)
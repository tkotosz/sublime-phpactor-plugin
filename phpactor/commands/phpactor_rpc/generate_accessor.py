import sublime_plugin

class PhpactorGenerateAccessorCommand(sublime_plugin.TextCommand):
    def run(self, edit, names=None):
        request = {
            'action': 'generate_accessor',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset'
            }
        }
        self.view.run_command('phpactor_rpc', request)
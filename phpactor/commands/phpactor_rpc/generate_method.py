import sublime_plugin

class PhpactorGenerateMethodCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'generate_method',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset'
            }
        }
        self.view.run_command('phpactor_rpc', request)
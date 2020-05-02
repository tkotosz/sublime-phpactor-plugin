import sublime_plugin

class PhpactorExtractConstantCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'extract_constant',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset'
            }
        }
        self.view.run_command('phpactor_rpc', request)
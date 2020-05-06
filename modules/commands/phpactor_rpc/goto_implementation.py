import sublime_plugin

class PhpactorGotoImplementationCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'goto_implementation',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset',
                'target': 'focused_window',
                'language': '@current_language'
            }
        }
        self.view.run_command('phpactor_rpc', request)
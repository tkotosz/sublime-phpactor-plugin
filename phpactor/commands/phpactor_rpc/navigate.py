import sublime_plugin

class PhpactorNavigateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'navigate',
            'parameters': {
                'source_path': '@current_path'
            }
        }
        self.view.run_command('phpactor_rpc', request)
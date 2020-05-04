import sublime_plugin

class PhpactorClassNewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'class_new',
            'parameters': {
                'current_path': '@current_path'
            }
        }
        self.view.run_command('phpactor_rpc', request)
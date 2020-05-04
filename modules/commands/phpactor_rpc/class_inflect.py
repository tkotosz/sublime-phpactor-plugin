import sublime_plugin

class PhpactorClassInflectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'class_inflect',
            'parameters': {
                'current_path': '@current_path'
            }
        }
        self.view.run_command('phpactor_rpc', request)
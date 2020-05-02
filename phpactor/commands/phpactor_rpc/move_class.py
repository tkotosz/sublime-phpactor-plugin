import sublime_plugin

class PhpactorMoveClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'move_class',
            'parameters': {
                'source_path': '@current_path'
            }
        }
        self.view.run_command('phpactor_rpc', request)
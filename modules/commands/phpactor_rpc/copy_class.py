import sublime_plugin

class PhpactorCopyClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'copy_class',
            'parameters': {
                'source_path': '@current_path'
            }
        }
        self.view.run_command('phpactor_rpc', request)
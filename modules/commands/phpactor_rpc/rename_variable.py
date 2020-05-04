import sublime_plugin

class PhpactorRenameVariableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'rename_variable',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset'
            }
        }
        self.view.run_command('phpactor_rpc', request)
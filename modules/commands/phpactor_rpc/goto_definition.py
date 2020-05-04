import sublime_plugin

class PhpactorGotoDefinitionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'goto_definition',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset',
                'target': 'focused_window'
            }
        }

        self.view.run_command('phpactor_rpc', request)
import sublime_plugin

class PhpactorContextMenuCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'context_menu',
            'parameters': {
                'source': '@current_source',
                'current_path': '@current_path',
                'offset': '@current_offset'
            }
        }
        self.view.run_command('phpactor_rpc', request)
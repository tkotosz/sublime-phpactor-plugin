import sublime_plugin

class PhpactorOffsetInfoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'offset_info',
            'parameters': {
                'source': '@current_source',
                'offset': '@current_offset'
            }
        }
        self.view.run_command('phpactor_rpc', request)
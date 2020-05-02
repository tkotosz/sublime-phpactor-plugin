import sublime_plugin

class PhpactorEchoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'echo',
            'parameters': {
                'message': 'Phpactor Status: OK'
            }
        }
        self.view.run_command('phpactor_rpc', request)
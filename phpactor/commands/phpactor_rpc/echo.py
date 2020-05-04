import sublime_plugin

class PhpactorEchoCommand(sublime_plugin.TextCommand):
    def run(self, edit, message = 'Phpactor Status: OK'):
        request = {
            'action': 'echo',
            'parameters': {
                'message': message
            }
        }
        self.view.run_command('phpactor_rpc', request)
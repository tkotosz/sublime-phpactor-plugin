import sublime_plugin

class PhpactorFileInfoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'file_info',
            'parameters': {
                'path': '@current_path'
            }
        }

        # TODO - This returns a "return" editor action which should be consumed directly then anything can done with it
        self.view.run_command('phpactor_rpc', request)
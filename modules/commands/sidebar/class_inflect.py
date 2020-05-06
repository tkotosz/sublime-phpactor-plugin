import sublime_plugin

class PhpactorSidebarClassInflectCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        request = {
            'action': 'class_inflect',
            'parameters': {
                'current_path': files[0]
            }
        }
        self.window.active_view().run_command('phpactor_rpc', request)

    def is_visible(self, files):
        return len(files) == 1
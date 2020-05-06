import sublime_plugin

class PhpactorSidebarMoveClassCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        request = {
            'action': 'move_class',
            'parameters': {
                'source_path': files[0]
            }
        }
        self.window.active_view().run_command('phpactor_rpc', request)

    def is_visible(self, files):
        return len(files) == 1
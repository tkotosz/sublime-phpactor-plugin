import sublime_plugin

class PhpactorImportMissingClassesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'import_missing_classes',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path'
            }
        }
        self.view.run_command('phpactor_rpc', request)
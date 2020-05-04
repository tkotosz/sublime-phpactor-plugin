import sublime_plugin

class PhpactorExtractExpressionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'extract_expression',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset_start': '@current_offset_start',
                'offset_end': '@current_offset_end'
            }
        }
        self.view.run_command('phpactor_rpc', request)
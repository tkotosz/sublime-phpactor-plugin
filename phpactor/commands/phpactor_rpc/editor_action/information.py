import sublime
import sublime_plugin

class PhpactorEditorActionInformationCommand(sublime_plugin.TextCommand):
    def run(self, edit, information):
        debug_view = self.view.window().create_output_panel('phpactor_information')
        debug_view.set_syntax_file('Packages/JavaScript/JSON.sublime-syntax')
        debug_view.insert(edit, 0, information)
        self.view.window().run_command('show_panel', { 'panel': 'output.phpactor_information' })
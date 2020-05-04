import sublime
import sublime_plugin

class PhpactorEditorActionCloseFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, path):
        self.view.window().run_command('tk_close_file', { 'file_path': path } )
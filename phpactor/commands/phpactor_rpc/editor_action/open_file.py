import sublime
import sublime_plugin

class PhpactorEditorActionOpenFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, force_reload, path, offset, target):
        # navigate command returns relative path for some reason
        if path.find('/') != 0:
            path = tksublime.find_working_dir(view) + '/' + path

        self.view.window().run_command('tk_open_file_at_offset', { 'file_path': path, 'offset': offset } )
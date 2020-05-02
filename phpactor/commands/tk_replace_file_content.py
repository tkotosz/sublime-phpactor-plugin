import sublime
import sublime_plugin

class TkReplaceFileContentCommand(sublime_plugin.TextCommand):
    def run(self, edit, file_path, source):
        self.view.window().run_command('tk_open_file', { 'file_path': file_path })
        file_view = self.view.window().find_open_file(file_path)
        if file_view: # something went wrong while opening the file
            file_view.replace(edit, sublime.Region(0, file_view.size()), source)
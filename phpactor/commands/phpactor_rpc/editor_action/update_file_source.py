import sublime
import sublime_plugin

class PhpactorEditorActionUpdateFileSourceCommand(sublime_plugin.TextCommand):
    def run(self, edit, path, edits, source):
        # TODO FIX cursor position after source update
        self.view.run_command('tk_replace_file_content', { 'file_path': path, 'source': source } )
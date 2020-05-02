import sublime
import sublime_plugin

class PhpactorEditorActionErrorCommand(sublime_plugin.TextCommand):
    def run(self, edit, message, details):
        sublime.run_command('tk_show_status_message', { 'message': 'Phpactor Error: ' + message })
import sublime
import sublime_plugin

class PhpactorEditorActionEchoCommand(sublime_plugin.TextCommand):
    def run(self, edit, message = "Hello"):
        sublime.run_command('tk_show_status_message', { 'message': message })
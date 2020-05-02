import sublime
import sublime_plugin

class TkShowStatusMessageCommand(sublime_plugin.ApplicationCommand):
    def run(self, message):
        sublime.status_message(message)
import sublime
import sublime_plugin

class TkOpenFilePreviewCommand(sublime_plugin.WindowCommand):
    def run(self, file_path):
        self.window.open_file(file_path, sublime.TRANSIENT | sublime.ENCODED_POSITION | sublime.FORCE_GROUP, self.window.active_group())
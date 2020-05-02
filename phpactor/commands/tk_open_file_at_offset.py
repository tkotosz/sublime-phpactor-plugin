import sublime
import sublime_plugin

class TkOpenFileAtOffsetCommand(sublime_plugin.WindowCommand):
    def run(self, file_path, offset):
        self.window.run_command('tk_open_file', { 'file_path': file_path })
        self.window.run_command('tk_jump_to_offset', { 'offset': offset })
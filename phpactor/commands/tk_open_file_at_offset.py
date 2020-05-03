import sublime
import sublime_plugin

class TkOpenFileAtOffsetCommand(sublime_plugin.TextCommand):
    def run(self, edit, file_path, offset):
        if self.view.file_name() != file_path:
            self.view.window().open_file(file_path, sublime.ENCODED_POSITION | sublime.FORCE_GROUP, self.view.window().active_group())
            self.view.window().run_command(
                'tk_run_command_when_file_loaded',
                {
                    'file_path': file_path,
                    'command_name': 'tk_open_file_at_offset',
                    'command_params': { 'file_path': file_path, 'offset': offset }
                }
            );
            return

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(offset))
        sublime.set_timeout(lambda: self.view.show_at_center(offset), 0)
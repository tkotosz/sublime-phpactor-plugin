import sublime
import sublime_plugin

class TkOpenFileAtOffsetCommand(sublime_plugin.TextCommand):
    def run(self, edit, file_path, offset):
        file_view = self.get_file_view(file_path)

        if not file_view:
            return

        if file_view.is_loading(): # we need to wait, the file is loading
            print("schedule")
            file_view.window().run_command(
                'tk_run_command_when_file_loaded',
                {
                    'file_path': file_path,
                    'command_name': 'tk_jump_to_offset',
                    'command_params': { 'offset': offset }
                }
            );
            return

        file_view.sel().clear()
        file_view.sel().add(sublime.Region(offset))
        sublime.set_timeout(lambda: file_view.show_at_center(offset), 0)

    def get_file_view(self, path):
        if self.view.file_name() == path:
            return self.view

        self.view.window().run_command('tk_open_file', { 'file_path': path })
        return self.view.window().find_open_file(path)
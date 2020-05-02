import sublime
import sublime_plugin

class PhpactorEditorActionUpdateFileSourceCommand(sublime_plugin.TextCommand):
    def run(self, edit, path, edits, source):
        file_view = self.get_file_view(path)

        if not file_view:
            return

        if file_view.is_loading(): # we need to wait, the file was not open already
            self.view.window().run_command(
                'tk_run_command_when_file_loaded',
                {
                    'file_path': path,
                    'command_name': 'phpactor_editor_action_update_file_source',
                    'command_params': { 'path': path, 'edits': edits, 'source': source }
                }
            );
            return

        original_selections = [r for r in file_view.sel()]
        restore_original_position = False
        for e in edits:
            startPoint = file_view.text_point(e['start']['line'], e['start']['character'])
            endPoint = file_view.text_point(e['end']['line'], e['end']['character'])
            content = e['text']
            region = sublime.Region(startPoint, endPoint)

            if e['text'] == '' and self.contains_the_cursor(file_view, region): # deleting some lines
                restore_original_position = True

            file_view.replace(edit, region, content)

        if restore_original_position:
            file_view.sel().clear()
            file_view.sel().add_all(original_selections)

    def get_file_view(self, path):
        if self.view.file_name() == path:
            return self.view

        self.view.window().run_command('tk_open_file', { 'file_path': path })
        return self.view.window().find_open_file(path)

    def contains_the_cursor(self, file_view, edit_region):
        for region in file_view.sel():
            if region.intersects(edit_region):
                return True

        return False
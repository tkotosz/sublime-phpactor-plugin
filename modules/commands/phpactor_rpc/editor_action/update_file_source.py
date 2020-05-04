import sublime
import sublime_plugin

class PhpactorEditorActionUpdateFileSourceCommand(sublime_plugin.TextCommand):
    def run(self, edit, path, edits, source):
        if self.view.file_name() != path:
            self.view.window().open_file(path, sublime.ENCODED_POSITION | sublime.FORCE_GROUP, self.view.window().active_group())
            self.view.window().run_command(
                'tk_run_command_when_file_loaded',
                {
                    'file_path': path,
                    'command_name': 'phpactor_editor_action_update_file_source',
                    'command_params': { 'path': path, 'edits': edits, 'source': source }
                }
            );
            return
        
        file_view = self.view

        if not edits: # if no edits returned then apply the changed source (- fix for Replace References)
            file_view.replace(edit, sublime.Region(0, file_view.size()), source)
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

    def contains_the_cursor(self, file_view, edit_region):
        for region in file_view.sel():
            if region.intersects(edit_region):
                return True

        return False
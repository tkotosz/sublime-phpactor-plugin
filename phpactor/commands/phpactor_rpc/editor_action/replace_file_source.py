import sublime
import sublime_plugin

class PhpactorEditorActionReplaceFileSourceCommand(sublime_plugin.TextCommand):
    def run(self, edit, path, source):
        if self.view.file_name() != path:
            self.view.window().open_file(path, sublime.ENCODED_POSITION | sublime.FORCE_GROUP, self.view.window().active_group())
            self.view.window().run_command(
                'tk_run_command_when_file_loaded',
                {
                    'file_path': path,
                    'command_name': 'phpactor_editor_action_replace_file_source',
                    'command_params': { 'path': path, 'edits': edits, 'source': source }
                }
            );
            return
        
        self.view.replace(edit, sublime.Region(0, self.view.size()), source)
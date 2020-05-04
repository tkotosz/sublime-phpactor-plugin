import sublime
import sublime_plugin
import os
from ....utils import *

class PhpactorEditorActionFileReferencesCommand(sublime_plugin.TextCommand):
    def run(self, edit, file_references):
        window = self.view.window();
        original_selections = [r for r in self.view.sel()]

        files = []
        options = []
        for file_reference in file_references:
            for line_reference in file_reference['references']:
                pos = ":" + str(line_reference['line_no']) + ":" + str(line_reference['col_no'] + 1) # col starts from 1 in sublime, api returns from 0
                file_name = os.path.basename(file_reference['file'])
                file_absolute_path = file_reference['file']
                file_relative_path = file_absolute_path.replace(find_working_dir(self.view) + '/', '')
                files.append(file_absolute_path + pos);
                options.append([file_name + pos, file_relative_path + pos])
        
        window.show_quick_panel(
            options,
            on_select=lambda index: self.open_file(index, files, window, self.view, original_selections),
            on_highlight=lambda index: self.show_preview(index, files, window)
        )

    def open_file(self, index, files, window, original_view, original_selections):
        if index == -1:
            # restore original view
            original_view.sel().clear()
            original_view.sel().add_all(original_selections)
            window.focus_view(original_view)
            original_view.show(original_selections[0])
            return

        window.run_command('tk_open_file', { 'file_path': files[index] })

    def show_preview(self, index, files, window):
        window.run_command('tk_open_file_preview', { 'file_path': files[index] })
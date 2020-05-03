import sublime
import sublime_plugin

class TkOpenFileAtOffsetCommand(sublime_plugin.TextCommand):
    def run(self, edit, file_path, offset):
        self.view.window().open_file(file_path, sublime.ENCODED_POSITION | sublime.FORCE_GROUP, self.view.window().active_group())
        sublime.set_timeout_async(lambda: self.jump_to_offset(file_path, offset))

    def jump_to_offset(self, file_path, offset):
        file_view = self.view.window().find_open_file(file_path)
        region = sublime.Region(offset, offset)
        self.view.window().focus_view(file_view)
        file_view.sel().clear()
        file_view.sel().add(region)
        file_view.show_at_center(region)
        
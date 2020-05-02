import sublime
import sublime_plugin

class TkJumpToOffsetCommand(sublime_plugin.WindowCommand):
    view = None
    offset = 0
    def run(self, offset):
        view = self.window.active_view();
        if view.is_loading(): # need to wait for file open (see TkJumpToOffsetFileOpenedEventListener)
            TkJumpToOffsetCommand.view = view
            TkJumpToOffsetCommand.offset = int(offset)
            return;

        view.sel().clear()
        view.sel().add(sublime.Region(offset))
        sublime.set_timeout(lambda: view.show_at_center(offset), 0)

class TkJumpToOffsetFileOpenedEventListener(sublime_plugin.EventListener):
    # very weird but only "on_load_async" + "set_timeout" combination works reliably for some reason :/
    def on_load_async(self,view):
        if view == TkJumpToOffsetCommand.view:
            offset = TkJumpToOffsetCommand.offset
            view.sel().clear()
            view.sel().add(sublime.Region(offset))
            sublime.set_timeout(lambda: view.show_at_center(offset), 0)
            TkJumpToOffsetCommand.file_path = ''
            TkJumpToOffsetCommand.offset = ''
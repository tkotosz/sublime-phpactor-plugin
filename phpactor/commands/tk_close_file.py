import sublime
import sublime_plugin

class TkCloseFileCommand(sublime_plugin.WindowCommand):
    def run(self, file_path):
        file_view = self.window.find_open_file(file_path)
        
        if not file_view:
        	return

        file_view.close() # undocumented function but exists! (otherwise I would have to switch to it, trigger a close current file then switch back)
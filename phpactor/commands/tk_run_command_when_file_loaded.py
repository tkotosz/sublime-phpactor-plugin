import sublime
import sublime_plugin

class TkRunCommandWhenFileLoaded(sublime_plugin.WindowCommand):
    notify_queue = {}
    def run(self, file_path, command_name, command_params):
        queue = TkRunCommandWhenFileLoaded.notify_queue

        file_view = self.window.find_open_file(file_path)

        if not file_view: # it is not opened at all
            return

        if not file_view.is_loading(): # already loaded
            file_view.run_command(command_name, command_params)
            return;

        if not file_path in queue:
            queue[file_path] = []

        queue[file_path] = {'command_name': command_name, 'command_params': command_params}

class TkRunCommandWhenFileLoadedListener(sublime_plugin.EventListener):
    def on_load_async(self,view):
        current_file_path = view.file_name()
        queue = TkRunCommandWhenFileLoaded.notify_queue.copy()
        for file_path in queue:
          if file_path == current_file_path:
            command = queue[file_path]
            del TkRunCommandWhenFileLoaded.notify_queue[file_path]
            view.run_command(command['command_name'], command['command_params'])
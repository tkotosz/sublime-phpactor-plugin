import sublime
import sublime_plugin

class TkRunCommandWhenFileLoaded(sublime_plugin.WindowCommand):
    notify_queue = {}
    def run(self, file_path, command_name, command_params):
        queue = TkRunCommandWhenFileLoaded.notify_queue

        if not file_path in queue:
            queue[file_path] = []

        queue[file_path].append({'command_name': command_name, 'command_params': command_params})

class TkRunCommandWhenFileLoadedListener(sublime_plugin.EventListener):
    def on_load_async(self,view):
        current_file_path = view.file_name()
        queue = TkRunCommandWhenFileLoaded.notify_queue.copy()
        for file_path in queue:
          if file_path == current_file_path:
            commands = queue[file_path]
            del TkRunCommandWhenFileLoaded.notify_queue[file_path]
            for command in commands:
                print('calling', command)
                view.run_command(command['command_name'], command['command_params'])
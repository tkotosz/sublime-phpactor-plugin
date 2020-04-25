import sublime
import sublime_plugin
import os
from subprocess import PIPE, Popen
import json

class SublimeApi:
    def get_phpactor_settings(self, view):
        return Phpactor.Settings(
            self.get_phpactor_bin(),
            self.get_working_dir(view)
        )

    def apply_rpc_action(self, view, action_name, parameters):
        if action_name == 'collection':
            for action in parameters['actions']:
                view.run_command('phpactor_sublime_' + action['name'], action['parameters'])
        else:
            view.run_command('phpactor_sublime_' + action_name, parameters)

    def insert_to_current_positions(self, view, edit, text):
        for region in view.sel():
            view.insert(edit, region.begin(), text)

    def update_status_message(self, message):
        sublime.status_message(message)

    def show_quick_panel(self, view, items, on_select, on_highlight):
        view.window().show_quick_panel(items, on_select, on_highlight=on_highlight)

    def open_file(self, view, file_path, preview_mode = 0):
        flags = 0
        
        if file_path.find(":") != -1:
            flags |= sublime.ENCODED_POSITION

        if preview_mode:
            flags |= sublime.TRANSIENT | getattr(sublime, 'FORCE_GROUP', 0)

        return view.window().open_file(file_path, flags)

    def get_current_position(self, view):
        for region in view.sel():
            return view.line(region).begin()

    def get_current_line(self, view):
        for region in view.sel():
            return view.substr(view.line(region))

    def get_current_file_content(self, view):
        return view.substr(sublime.Region(0, view.size()))

    def get_current_file_path(self, view):
        return view.file_name()

    def log_rpc_sent(self, request):
        self.log('--> phpactor(rpc)', request.to_json())

    def log_rpc_received(self, response):
        self.log('<-- phpactor(rpc)', response.to_json())

    def log(self, *message):
        print("[SUBLIME-PHPACTOR]", *message)

    def log_error(self, *message):
        print("[SUBLIME-PHPACTOR] Error:", *message)

    def get_phpactor_bin(self):
        return '/home/tkotosz/Sites/phpactor/bin/phpactor' #todo

    def get_working_dir(self, view):
        for folder in view.window().folders():
            if os.path.isfile(folder + '/composer.json'):
                return folder
        return None

class Phpactor:
    class Settings:
        def __init__(self, phpactorbin, project_root):
            self.phpactorbin = phpactorbin
            self.project_root = project_root

    class Rpc:
        class Request:
            def __init__(self, action, parameters):
                self.action = action
                self.parameters = parameters

            def to_json(self):
                return json.dumps(self, default=lambda o: o.__dict__)

        class Response:
            def __init__(self, action, parameters):
                self.action = action
                self.parameters = parameters

            def from_json(value):
                d = json.loads(value.decode())
                return Phpactor.Rpc.Response(d['action'], d['parameters'])

            def to_json(self):
                return json.dumps(self, default=lambda o: o.__dict__)

        class GeneralError:
            def __init__(self, message):
                self.message = message

        class Client:
            def __init__(self, phpactorbin, project_root):
                self.phpactorbin = phpactorbin
                self.project_root = project_root

            def send(self, request):
                p = Popen([self.phpactorbin, 'rpc'], stdout=PIPE, stdin=PIPE, stderr=PIPE, cwd=self.project_root)
                stdout, stderr = p.communicate(request.to_json().encode())

                if stderr:
                    return None, Phpactor.Rpc.GeneralError(stderr)

                return Phpactor.Rpc.Response.from_json(stdout), None

    def __init__(self, settings):
        self.rpc_client = Phpactor.Rpc.Client(settings.phpactorbin, settings.project_root)

    def send_rpc_request(self, request):
        return self.rpc_client.send(request)

class PhpactorEchoCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)
        self.sublime_api = SublimeApi()

    def run(self, edit, message = "Hello"):
        phpactor = Phpactor(self.sublime_api.get_phpactor_settings(self.view))
        request = Phpactor.Rpc.Request('echo', { "message": message })
        self.sublime_api.log_rpc_sent(request)
        response, err = phpactor.send_rpc_request(request)

        if err:
            self.sublime_api.log_error(err.message)
            return;

        self.sublime_api.log_rpc_received(response)

        self.sublime_api.apply_rpc_action(self.view, response.action, response.parameters)

class PhpactorReferencesCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)
        self.sublime_api = SublimeApi()

    def run(self, edit, message = "Hello"):
        phpactor = Phpactor(self.sublime_api.get_phpactor_settings(self.view))
        offset = self.sublime_api.get_current_position(self.view)
        source = self.sublime_api.get_current_file_content(self.view)
        path = self.sublime_api.get_current_file_path(self.view)
        request = Phpactor.Rpc.Request('references', { "offset": offset, "source": source, "path": path })
        self.sublime_api.log_rpc_sent(request)
        
        response, err = phpactor.send_rpc_request(request)

        if err:
            self.sublime_api.log_error(err.message)
            return;

        self.sublime_api.log_rpc_received(response)

        self.sublime_api.apply_rpc_action(self.view, response.action, response.parameters)

class PhpactorSublimeEchoCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)
        self.sublime_api = SublimeApi()

    def run(self, edit, message = "Hello"):
        self.sublime_api.update_status_message(message)

class PhpactorSublimeErrorCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)
        self.sublime_api = SublimeApi()

    def run(self, edit, message, details):
        self.sublime_api.update_status_message("Phpactor Error: " + message)

class PhpactorSublimeFileReferencesCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)
        self.sublime_api = SublimeApi()

    def run(self, edit, file_references):
        self.files = []
        for file_reference in file_references:
            for line_reference in file_reference['references']:
                line = str(line_reference['line_no'])
                file_name = os.path.basename(file_reference['file'])
                file_path = file_reference['file']
                info = [file_name + ":" + line, file_path]
                self.files.append(info)

        self.sublime_api.show_quick_panel(self.view, self.files, self.open_file, self.show_preview)

    def open_file(self, index):
        if index == -1:
            #self.close_preview()
            return

        self.sublime_api.open_file(self.view, os.path.dirname(self.files[index][1]) + "/" + self.files[index][0]);
        #self.view.window().open_file(os.path.dirname(self.files[index][1]) + "/" + self.files[index][0], sublime.ENCODED_POSITION)

    def close_preview(self):
        if not self.preview:
            return

        if self.view.window().get_view_index(self.preview)[1] == -1: # preview is open (it has no tab)
            self.view.window().run_command("close_file")

    def show_preview(self, index):
        self.preview = self.sublime_api.open_file(self.view, os.path.dirname(self.files[index][1]) + "/" + self.files[index][0], 1);

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

    def open_file(self, view, file_path):
        flags = 0
        
        if file_path.find(":") != -1:
            flags |= sublime.ENCODED_POSITION

        return view.window().open_file(file_path, flags)

    def open_file_preview(self, view, file_path):
        flags = sublime.TRANSIENT | getattr(sublime, 'FORCE_GROUP', 0)

        if file_path.find(":") != -1:
            flags |= sublime.ENCODED_POSITION

        return view.window().open_file(file_path, flags)

    def close_file_preview(self, view, file):
        if not file:
            return

        if view.window().get_view_index(file)[1] == -1: # it is a file open for preview if it has no tab
            view.window().run_command("close_file")

    def get_current_selections(self, view):
        return [(selection.begin(), selection.end()) for selection in view.sel()]

    def set_selections(self, view, selections):
        view.sel().clear()
        for selection in selections:
            view.sel().add(sublime.Region(selection[0], selection[1]))
            view.show_at_center(selection[0])

    def set_current_position_by_byte_offset(self, view, offset):
        view.sel().clear()
        view.sel().add(sublime.Region(offset))
        sublime.set_timeout(lambda: view.show_at_center(offset), 0)

    def get_current_position(self, view):
        for region in view.sel():
            return region.begin()

    def get_current_line(self, view):
        for region in view.sel():
            return view.substr(view.line(region))

    def get_current_file_content(self, view):
        return view.substr(sublime.Region(0, view.size()))

    def get_current_file_path(self, view):
        file_path = view.file_name();

        if file_path:
            return file_path

        return "" # unsaved file

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
        current_file_path = view.file_name()

        if current_file_path:
            for folder in view.window().folders():
                if current_file_path.find(folder) == 0:
                    return folder # root folder of the file must be the "project" root

            return os.path.dirname(current_file_path) # single file opened in sublime, lets use it's folder as working dir
        else: # unsaved file
            for folder in view.window().folders():
                return folder # assume that it belongs to the first folder

        return None # unsaved file & no folder open in the sidebar


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

        print(self.sublime_api.get_current_position(self.view))

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

    def run(self, edit):
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

class PhpactorGotoDefinitionCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)
        self.sublime_api = SublimeApi()

    def run(self, edit):
        phpactor = Phpactor(self.sublime_api.get_phpactor_settings(self.view))
        offset = self.sublime_api.get_current_position(self.view)
        source = self.sublime_api.get_current_file_content(self.view)
        path = self.sublime_api.get_current_file_path(self.view)
        request = Phpactor.Rpc.Request('goto_definition', { "offset": offset, "source": source, "path": path, "target": "focused_window" })
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
        options = []
        self.selections_before = self.sublime_api.get_current_selections(self.view)
        self.file_before = self.sublime_api.get_current_file_path(self.view)
        for file_reference in file_references:
            for line_reference in file_reference['references']:
                pos = ":" + str(line_reference['line_no']) + ":" + str(line_reference['col_no'] + 1) # col starts from 1 in sublime, api returns from 0
                file_name = os.path.basename(file_reference['file'])
                file_absolute_path = file_reference['file']
                file_relative_path = file_absolute_path.replace(self.sublime_api.get_working_dir(self.view) + '/', '')
                self.files.append(file_absolute_path + pos);
                options.append([file_name + pos, file_relative_path + pos])

        self.sublime_api.show_quick_panel(self.view, options, self.open_file, self.show_preview)

    def open_file(self, index):
        if index == -1:
            self.sublime_api.close_file_preview(self.view, self.preview_file) # close preview
            self.sublime_api.open_file(self.view, self.file_before) # restore file view
            self.sublime_api.set_selections(self.view, self.selections_before) # restore previous selection
            return

        self.sublime_api.open_file(self.view, self.files[index]); # jump to file

    def show_preview(self, index):
        self.preview_file = self.sublime_api.open_file_preview(self.view, self.files[index]);

class PhpactorSublimeOpenFileCommand(sublime_plugin.TextCommand):
    view = None
    offset = 0
    def __init__(self, view):
        super().__init__(view)
        self.sublime_api = SublimeApi()

    def run(self, edit, force_reload, path, offset, target):
        file_view = self.sublime_api.open_file(self.view, path)
        
        if file_view.is_loading(): # need to wait for file open (see PhpactorSublimeOpenFileCommandFileOpenedEventListener)
            PhpactorSublimeOpenFileCommand.view = file_view
            PhpactorSublimeOpenFileCommand.offset = offset
            return;

        self.sublime_api.set_current_position_by_byte_offset(file_view, offset)

class PhpactorSublimeOpenFileCommandFileOpenedEventListener(sublime_plugin.EventListener):
    def on_load_async(self,view):
        if view == PhpactorSublimeOpenFileCommand.view:
            SublimeApi().set_current_position_by_byte_offset(view, PhpactorSublimeOpenFileCommand.offset)
            PhpactorSublimeOpenFileCommand.file_path = ''
            PhpactorSublimeOpenFileCommand.offset = ''
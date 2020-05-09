from subprocess import PIPE, Popen
import json
from .utils import *
from .settings import *

class Phpactor:
    class Rpc:
        class Request:
            def __init__(self, action, parameters):
                self.action = action
                self.parameters = parameters

            def path(self):
                if 'path' in self.parameters:
                    return self.parameters['path']

                if 'current_path' in self.parameters:
                    return self.parameters['current_path']

                if 'source_path' in self.parameters:
                    return self.parameters['source_path']

                return None

            def to_json(self):
                return json.dumps({'action': self.action, 'parameters': self.parameters}, sort_keys=True)

        class Response:
            def __init__(self, action, parameters):
                self.action = action
                self.parameters = parameters

            def from_json(value):
                d = json.loads(value)
                return Phpactor.Rpc.Response(d['action'], d['parameters'])

            def to_json(self):
                return json.dumps({'action': self.action, 'parameters': self.parameters}, sort_keys=True)

        class Client:
            def __init__(self, phpactorbin, project_root):
                self.phpactorbin = phpactorbin
                self.project_root = project_root

            def send(self, request):
                p = Popen([self.phpactorbin, 'rpc'], stdout=PIPE, stdin=PIPE, stderr=PIPE, cwd=self.project_root)
                stdout, stderr = p.communicate(request.to_json().encode())

                if stderr:
                    return Phpactor.Rpc.Response('error', { 'message': 'RPC request failed with unknown error', 'details': stderr.decode() })

                return Phpactor.Rpc.Response.from_json(stdout.decode())

    def __init__(self, window):
        self.window = window

    def send_rpc_request(self, request):
        request = self.replace_request_parameter_placeholders(request)
        rpc_client = Phpactor.Rpc.Client(get_phpactor_bin(), find_working_dir(self.window, request.path()))

        log_rpc_request(request)

        response = rpc_client.send(request)

        log_rpc_response(response)

        return self.dispatch_rpc_editor_action(response)

    def dispatch_rpc_editor_action(self, response):
        if response.action == 'return':
            return response.parameters['value']

        if response.action == 'return_choice':
            return response.parameters['choices']  # TODO

        self.window.active_view().run_command('phpactor_dispatch_rpc_editor_action', { 'name': response.action, 'parameters': response.parameters })
        return None

    def replace_request_parameter_placeholders(self, request):
        replaceMap = {
            'current_source': self.get_current_file_content(),
            'current_path': self.get_current_file_path(),
            'current_offset': self.get_current_position(),
            'current_offset_start': self.get_current_position_start(),
            'current_offset_end': self.get_current_position_end(),
            'current_language': self.get_current_language()
        }

        for key in request.parameters:
            if isinstance(request.parameters[key], str) or isinstance(request.parameters[key], int):
                for placeholder in replaceMap:
                    request.parameters[key] = str(request.parameters[key]).replace('@'+placeholder, str(replaceMap[placeholder]))

        for key in ['offset', 'offset_start', 'offset_end']:
            if key in request.parameters:
                request.parameters[key] = int(request.parameters[key])

        return request

    def get_current_position(self):
        for region in self.window.active_view().sel():
            return region.begin()

    def get_current_position_start(self):
        for region in self.window.active_view().sel():
            return region.begin()

    def get_current_position_end(self):
        for region in self.window.active_view().sel():
            return region.end()

    def get_current_file_content(self):
        return self.window.active_view().substr(sublime.Region(0, self.window.active_view().size()))

    def get_current_file_path(self):
        file_path = self.window.active_view().file_name();

        if file_path:
            return file_path

        return "" # unsaved file

    def get_current_language(self):
        syntax = self.window.active_view().settings().get('syntax')
        language = syntax.rsplit("/", 1)[-1].split('.', 1)[0].lower()

        # Behat feature files are special they can have
        # "Gherkin", "Cucumber", "Behat", "Behat-Features" syntax depending on which syntax package is used
        # "gherkin", "cucumber" and "behat" are recognised by phpactor but "behat-features" is not
        if language == 'behat-features':
            language = 'gherkin'

        return language

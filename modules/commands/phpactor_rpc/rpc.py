import sublime
import sublime_plugin
from ...phpactor_client import *
from ...utils import *
from ...settings import *

class PhpactorRpcCommand(sublime_plugin.TextCommand):
    def run(self, edit, action, parameters):
        rpcRequest = self.build_rpc_request(action, parameters)
        phpactor = Phpactor(Phpactor.Settings(get_phpactor_bin(), find_working_dir(self.view, rpcRequest.path())))
        phpactor.send_rpc_request(self.build_rpc_request(action, parameters), self.before_send, self.on_error, self.on_done)

    def build_rpc_request(self, action, parameters):
        replaceMap = {
            'current_source': self.get_current_file_content(),
            'current_path': self.get_current_file_path(),
            'current_offset': self.get_current_position(),
            'current_offset_start': self.get_current_position_start(),
            'current_offset_end': self.get_current_position_end(),
            'current_language': self.get_current_language()
        }

        for key in parameters:
            if isinstance(parameters[key], str) or isinstance(parameters[key], int):
                for placeholder in replaceMap:
                    parameters[key] = str(parameters[key]).replace('@'+placeholder, str(replaceMap[placeholder]))

        for key in ['offset', 'offset_start', 'offset_end']:
            if key in parameters:
                parameters[key] = int(parameters[key])

        return Phpactor.Rpc.Request(action, parameters)

    def get_current_position(self):
        for region in self.view.sel():
            return region.begin()

    def get_current_position_start(self):
        for region in self.view.sel():
            return region.begin()

    def get_current_position_end(self):
        for region in self.view.sel():
            return region.end()

    def get_current_file_content(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def get_current_file_path(self):
        file_path = self.view.file_name();

        if file_path:
            return file_path

        return "" # unsaved file

    def get_current_language(self):
        syntax = self.view.settings().get('syntax')
        language = syntax.rsplit("/", 1)[-1].split('.', 1)[0].lower()

        # Behat feature files are special they can have
        # "Gherkin", "Cucumber", "Behat", "Behat-Features" syntax depending on which syntax package is used
        # "gherkin", "cucumber" and "behat" are recognised by phpactor but "behat-features" is not
        if language == 'behat-features':
            language = 'gherkin'

        return language

    def before_send(self, request):
        log_rpc_request(request)

    def on_error(self, err):
        log_rpc_error(err.message)
        self.dispatch_rpc_editor_action('error', { 'message': 'RPC request failed with unknown error (see logs)', 'details': err.message })

    def on_done(self, response):
        log_rpc_response(response)
        self.dispatch_rpc_editor_action(response.action, response.parameters)

    def dispatch_rpc_editor_action(self, name, parameters):
        self.view.run_command('phpactor_dispatch_rpc_editor_action', { 'name': name, 'parameters': parameters })

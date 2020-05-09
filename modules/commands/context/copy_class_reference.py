import sublime_plugin
import sublime
from ...settings import *
from ...utils import *
from ...phpactor_client import *

class PhpactorContextCopyClassReferenceCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        file_absolute_path = view.file_name();
        file_name = file_absolute_path.rsplit('/', 1)[-1].split('.', 1)[0]
        rpcRequest = Phpactor.Rpc.Request('class_search', { 'short_name': file_name })
        phpactor = Phpactor(Phpactor.Settings(get_phpactor_bin(), find_working_dir(self.window, file_absolute_path)))

        phpactor.send_rpc_request(rpcRequest, self.before_send, self.on_error, lambda response: self.on_done(response, file_absolute_path))

    def before_send(self, request):
        log_rpc_request(request)

    def on_error(self, err):
        log_rpc_error(err.message)
        self.dispatch_rpc_editor_action('error', { 'message': 'RPC request failed with unknown error (see logs)', 'details': err.message })

    def on_done(self, response, file_absolute_path):
        log_rpc_response(response)
        if response.action == 'return_choice':
        	for choice in response.parameters['choices']:
        		if choice['value']['file_path'] == file_absolute_path:
        			sublime.set_clipboard(choice['value']['class'])
        			return

        if response.action == 'return':
        	sublime.set_clipboard(response.parameters['value']['class'])
        	return

    def is_visible(self):
        return get_context_menu_setting('copy_class_reference', 'enabled', False)

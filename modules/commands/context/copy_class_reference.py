import sublime_plugin
import sublime
from ...settings import *
from ...phpactor_client import *

class PhpactorContextCopyClassReferenceCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        file_absolute_path = view.file_name();
        file_name = file_absolute_path.rsplit('/', 1)[-1].split('.', 1)[0]
        phpactor = Phpactor(self.window)
        rpcRequest = Phpactor.Rpc.Request('class_search', { 'short_name': file_name })
        result = phpactor.send_rpc_request(rpcRequest)

        if 'class' in result: # single match found
            sublime.set_clipboard(result['class'])
            return


        for key, item in result.items(): # multiple matches found
            if item['file_path'] == file_absolute_path:
                sublime.set_clipboard(item['class'])
                return

    def is_visible(self):
        return get_context_menu_setting('copy_class_reference', 'enabled', False) and self.window.active_view().file_name().find('.php') != -1

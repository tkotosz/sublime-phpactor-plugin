import sublime_plugin
from ...utils import log_editor_action

class PhpactorDispatchRpcEditorActionCommand(sublime_plugin.TextCommand):
    def run(self, edit, name, parameters):
        log_editor_action({'name': name, 'parameters': parameters})
        self.view.run_command('phpactor_editor_action_' + name, parameters)
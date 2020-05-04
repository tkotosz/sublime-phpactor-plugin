import sublime
import sublime_plugin

class PhpactorEditorActionCollectionCommand(sublime_plugin.TextCommand):
    def run(self, edit, actions):
        for action in actions:
            self.view.run_command('phpactor_dispatch_rpc_editor_action', action)
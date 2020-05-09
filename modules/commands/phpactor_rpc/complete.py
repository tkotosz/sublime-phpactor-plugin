import sublime_plugin
import sublime
from ...settings import *
from ...phpactor_client import *

class PhpactorComplete(sublime_plugin.ViewEventListener):
    @classmethod
    def is_applicable(cls, settings):
        return settings.get('syntax') == 'Packages/PHP/PHP.sublime-syntax'

    def on_query_completions(self, prefix, locations):
        if not get_command_setting('complete', 'enabled', False):
            return None

        phpactor = Phpactor(self.view.window())
        offset = locations[0]

        if not self.view.match_selector(offset, 'source.php | embedding.php'):
            return None

        # we will only deal with auto-complete with a single cursor for now
        if len(locations) != 1:
            return None;
        
        rpcRequest = Phpactor.Rpc.Request('complete', { 'source': '@current_source', 'offset': offset })
        result = phpactor.send_rpc_request(rpcRequest)

        matches = []
        for suggestion in result['suggestions']:
            trigger = suggestion['label'] + '\t' + suggestion['short_description']
            contents = suggestion['snippet']
            if not contents:
                contents = suggestion['label'].replace('$', '\\$')
            matches.append((trigger, contents))

        return (matches, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

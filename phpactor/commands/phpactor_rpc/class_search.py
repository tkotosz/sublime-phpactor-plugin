import sublime_plugin

class PhpactorClassSearchCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        keyword = self.get_current_word()

        if not keyword:
            return

        request = {
            'action': 'class_search',
            'parameters': {
                'short_name': keyword
            }
        }

        # TODO - This returns a "return_choice" editor action which should be consumed directly then anything can done with it
        self.view.run_command('phpactor_rpc', request)

    def get_current_word(self):
        keyword = ''
        for region in self.view.sel():
            if region.begin() == region.end():
                word = self.view.word(region)
            else:
                word = region

            if not word.empty():
                keyword = self.view.substr(word)
        
        return keyword
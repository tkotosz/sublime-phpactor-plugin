import sublime_plugin

# { "keys": ["<key>"], "command": "phpactor_transform", "args": { "transform": "complete_constructor" } },
# { "keys": ["<key>"], "command": "phpactor_transform", "args": { "transform": "add_missing_properties" } },
# { "keys": ["<key>"], "command": "phpactor_transform", "args": { "transform": "fix_namespace_class_name" } },
# { "keys": ["<key>"], "command": "phpactor_transform", "args": { "transform": "implement_contracts" } },
class PhpactorTransformCommand(sublime_plugin.TextCommand):
    def run(self, edit, transform = None):
        request = {
            'action': 'transform',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'transform': transform
            }
        }
        self.view.run_command('phpactor_rpc', request)
import sublime
import sublime_plugin

class PhpactorEditorActionInputCallbackCommand(sublime_plugin.TextCommand):
    def run(self, edit, inputs, callback):    
        input = inputs.pop(0)

        next = None
        if len(inputs) > 0: # we have more inputs
            next = lambda callback: self.view.run_command('phpactor_editor_action_input_callback', { 'inputs': inputs, 'callback': callback })

        if input['type'] == 'list':
            items = []

            if input['parameters']['multi']:
                items.append('All')

            for item in input['parameters']['choices']:
                items.append(item)

            self.view.window().show_quick_panel(
                items,
                on_select=lambda index: self.select_item(index, items, input['name'], input['parameters']['multi'], callback, next)
            )

        if input['type'] == 'choice':
            items = []

            for item in input['parameters']['choices']:
                items.append(item)

            self.view.window().show_quick_panel(
                items,
                on_select=lambda index: self.select_item(index, items, input['name'], False, callback, next)
            )

        if input['type'] == 'text':
            self.view.window().show_input_panel(
                input['parameters']['label'],
                input['parameters']['default'],
                lambda alias: self.handle_input(alias, input['name'], callback, next),
                None,
                None
            )

        if input['type'] == 'confirm':
            message = []
            for line in input['parameters']['label'].split('\n'):
                message.append(line.strip())

            callback['parameters'][input['name']] = sublime.ok_cancel_dialog('\n\n'.join(message), 'Confirm')

            if not next:
                self.view.run_command('phpactor_rpc', callback)
            else:
                next(callback)

    def select_item(self, index, items, property_name, is_multi, callback, next):
        if index == -1:
            return;

        if is_multi:
            if items[index] == 'All':
                del items[index]
                callback['parameters'][property_name] = items
            else:
                callback['parameters'][property_name] = [items[index]]
        else:
            callback['parameters'][property_name] = items[index]

        if not next:
            self.view.run_command('phpactor_rpc', callback)
        else:
            next(callback)

    def handle_input(self, alias, property_name, callback, next):
        callback['parameters'][property_name] = alias

        if not next:
            self.view.run_command('phpactor_rpc', callback)
        else:
            next(callback)
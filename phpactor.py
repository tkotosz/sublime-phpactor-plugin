import sublime
import sublime_plugin
import os
from subprocess import PIPE, Popen
import json

class SublimeApi:
    def get_phpactor_settings(self, view):
        return Phpactor.Settings(
            self.get_phpactor_bin(),
            self.get_working_dir(view)
        )

    def apply_rpc_action(self, view, action_name, parameters):
        self.log_editor_action({'name': action_name, 'parameters': parameters})
        view.run_command('phpactor_editor_action_' + action_name, parameters)

    def insert_to_current_positions(self, view, edit, text):
        for region in view.sel():
            view.insert(edit, region.begin(), text)

    def update_status_message(self, message):
        sublime.status_message(message)

    def show_quick_panel(self, view, items, on_select, on_highlight = None):
        view.window().show_quick_panel(items, on_select, on_highlight=on_highlight)

    def open_file(self, view, file_path):
        flags = 0
        
        if file_path.find(":") != -1:
            flags |= sublime.ENCODED_POSITION

        return view.window().open_file(file_path, flags)

    def open_file_preview(self, view, file_path):
        flags = sublime.TRANSIENT | getattr(sublime, 'FORCE_GROUP', 0)

        if file_path.find(":") != -1:
            flags |= sublime.ENCODED_POSITION

        return view.window().open_file(file_path, flags)

    def close_file_preview(self, view, file):
        if not file:
            return

        if view.window().get_view_index(file)[1] == -1: # it is a file open for preview if it has no tab
            view.window().run_command("close_file")

    def get_current_selections(self, view):
        return [(selection.begin(), selection.end()) for selection in view.sel()]

    def set_selections(self, view, selections):
        view.sel().clear()
        for selection in selections:
            view.sel().add(sublime.Region(selection[0], selection[1]))
            view.show_at_center(selection[0])

    def set_current_position_by_byte_offset(self, view, offset):
        view.sel().clear()
        view.sel().add(sublime.Region(offset))
        sublime.set_timeout(lambda: view.show_at_center(offset), 0)

    def get_current_position(self, view):
        for region in view.sel():
            return region.begin()

    def get_current_line(self, view):
        for region in view.sel():
            return view.substr(view.line(region))

    def get_current_file_content(self, view):
        return view.substr(sublime.Region(0, view.size()))

    def get_current_file_path(self, view):
        file_path = view.file_name();

        if file_path:
            return file_path

        return "" # unsaved file

    def log_rpc_request(self, request):
        self.log('--> phpactor(rpc)', request.to_json())

    def log_rpc_response(self, response):
        self.log('<-- phpactor(rpc)', response.to_json())

    def log_rpc_error(self, error):
        self.log('<-- phpactor(rpc)', error)

    def log_editor_action(self, action):
        self.log('--> sublime(editor-action)', action)

    def log(self, *message):
        print("[SUBLIME-PHPACTOR]", *message)

    def get_phpactor_bin(self):
        return '/home/tkotosz/Sites/phpactor/bin/phpactor' # TODO get this from settings

    def get_working_dir(self, view):
        current_file_path = view.file_name()

        if current_file_path:
            for folder in view.window().folders():
                if current_file_path.find(folder) == 0:
                    return folder # root folder of the file must be the "project" root

            return os.path.dirname(current_file_path) # single file opened in sublime, lets use it's folder as working dir
        else: # unsaved file
            for folder in view.window().folders():
                return folder # assume that it belongs to the first folder

        return None # unsaved file & no folder open in the sidebar


class Phpactor:
    class Settings:
        def __init__(self, phpactorbin, project_root):
            self.phpactorbin = phpactorbin
            self.project_root = project_root

    class Rpc:
        class Request:
            def __init__(self, action, parameters):
                self.action = action
                self.parameters = parameters

            def to_json(self):
                return json.dumps({'action': self.action, 'parameters': self.parameters}, sort_keys=True)

        class Response:
            def __init__(self, action, parameters):
                self.action = action
                self.parameters = parameters

            def from_json(value):
                d = json.loads(value.decode())
                return Phpactor.Rpc.Response(d['action'], d['parameters'])

            def to_json(self):
                return json.dumps({'action': self.action, 'parameters': self.parameters}, sort_keys=True)

        class GeneralError:
            def __init__(self, message):
                self.message = message

        class Client:
            def __init__(self, phpactorbin, project_root):
                self.phpactorbin = phpactorbin
                self.project_root = project_root

            def send(self, request):
                p = Popen([self.phpactorbin, 'rpc'], stdout=PIPE, stdin=PIPE, stderr=PIPE, cwd=self.project_root)
                stdout, stderr = p.communicate(request.to_json().encode())

                if stderr:
                    return None, Phpactor.Rpc.GeneralError(stderr)

                return Phpactor.Rpc.Response.from_json(stdout), None

    def __init__(self, settings):
        self.rpc_client = Phpactor.Rpc.Client(settings.phpactorbin, settings.project_root)

    def send_rpc_request(self, request, before_send, on_error, on_done):
        before_send(request)

        response, err = self.rpc_client.send(request)

        if err:
            on_error(err)
            return;

        on_done(response)

#################################################
# Public Commands [SUBLIME-PHPACTOR] -> Phpactor
#################################################

class PhpactorRpcCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)
        self.sublime_api = SublimeApi()

    def run(self, edit, action, parameters):
        phpactor = Phpactor(self.sublime_api.get_phpactor_settings(self.view))
        phpactor.send_rpc_request(self.create_request(action, parameters), self.before_send, self.on_error, self.on_done)

    def create_request(self, action, parameters):
        if 'source' in parameters:
            parameters['source'] = parameters['source'].replace('@current_source', self.sublime_api.get_current_file_content(self.view))

        if 'path' in parameters:
            parameters['path'] = parameters['path'].replace('@current_path', self.sublime_api.get_current_file_path(self.view))

        if 'offset' in parameters:
            parameters['offset'] = int(str(parameters['offset']).replace('@current_offset', str(self.sublime_api.get_current_position(self.view))))

        return Phpactor.Rpc.Request(action, parameters)

    def before_send(self, request):
        self.sublime_api.log_rpc_request(request)

    def on_error(self, err):
        self.sublime_api.log_rpc_error(err.message)
        self.sublime_api.apply_rpc_action(self.view, 'error', { 'message': 'RPC request failed with unknown error (see logs)', 'details': err.message })

    def on_done(self, response):
        self.sublime_api.log_rpc_response(response)
        self.sublime_api.apply_rpc_action(self.view, response.action, response.parameters)

class PhpactorEchoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'echo',
            'parameters': {
                'message': 'Phpactor Status: OK'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorReferencesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'references',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorGotoDefinitionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'goto_definition',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset',
                'target': 'focused_window'
            }
        }

        self.view.run_command('phpactor_rpc', request)

class PhpactorTransformCommand(sublime_plugin.TextCommand):
    def run(self, edit, transform):
        request = {
            'action': 'transform',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'transform': transform
            }
        }
        self.view.run_command('phpactor_rpc', request)


class PhpactorGenerateAccessorsCommand(sublime_plugin.TextCommand):
    def run(self, edit, names=None):
        request = {
            'action': 'generate_accessor',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorGenerateMethodCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'generate_method',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset'
            }
        }
        self.view.run_command('phpactor_rpc', request)

##################################################################
# Internal Commands (Editor Actions) [SUBLIME-PHPACTOR] -> Sublime
##################################################################

class PhpactorEditorActionEchoCommand(sublime_plugin.TextCommand):
    def run(self, edit, message = "Hello"):
        sublime.run_command('tk_show_status_message', { 'message': message })

class PhpactorEditorActionErrorCommand(sublime_plugin.TextCommand):
    def run(self, edit, message, details):
        sublime.run_command('tk_show_status_message', { 'message': 'Phpactor Error: ' + message })

class PhpactorEditorActionCollectionCommand(sublime_plugin.TextCommand):
    def run(self, edit, actions):
        for action in actions:
            self.view.run_command('phpactor_editor_action_' + action['name'], action['parameters'])

class PhpactorEditorActionFileReferencesCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)
        self.sublime_api = SublimeApi()

    def run(self, edit, file_references):
        window = self.view.window();
        original_selections = [r for r in self.view.sel()]

        files = []
        options = []
        for file_reference in file_references:
            for line_reference in file_reference['references']:
                pos = ":" + str(line_reference['line_no']) + ":" + str(line_reference['col_no'] + 1) # col starts from 1 in sublime, api returns from 0
                file_name = os.path.basename(file_reference['file'])
                file_absolute_path = file_reference['file']
                file_relative_path = file_absolute_path.replace(self.sublime_api.get_working_dir(self.view) + '/', '')
                files.append(file_absolute_path + pos);
                options.append([file_name + pos, file_relative_path + pos])
        
        window.show_quick_panel(
            options,
            on_select=lambda index: self.open_file(index, files, window, self.view, original_selections),
            on_highlight=lambda index: self.show_preview(index, files, window)
        )

    def open_file(self, index, files, window, original_view, original_selections):
        if index == -1:
            # restore original view
            original_view.sel().clear()
            original_view.sel().add_all(original_selections)
            window.focus_view(original_view)
            original_view.show(original_selections[0])
            return

        window.run_command('tk_open_file', { 'file_path': files[index] })

    def show_preview(self, index, files, window):
        window.run_command('tk_open_file_preview', { 'file_path': files[index] })

class PhpactorEditorActionOpenFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, force_reload, path, offset, target):
        self.view.window().run_command('tk_open_file_at_offset', { 'file_path': path, 'offset': offset } )

class PhpactorEditorActionInputCallbackCommand(sublime_plugin.TextCommand):
    def run(self, edit, inputs, callback):
        # TODO handle multiple inputs
        if len(inputs) > 1:
            return;

        for input in inputs:
            items = ['All']
            for item in input['parameters']['choices']:
                items.append(item)

            self.view.window().show_quick_panel(
                items,
                on_select=lambda index: self.select_item(index, items, input['name'], callback)
            )

    def select_item(self, index, items, property_name, callback):
        if index == -1:
            return;

        if items[index] == 'All':
            del items[index]
            callback['parameters'][property_name] = items
        else:
            callback['parameters'][property_name] = [items[index]]

        self.view.run_command('phpactor_rpc', callback)

class PhpactorEditorActionUpdateFileSourceCommand(sublime_plugin.TextCommand):
    def run(self, edit, path, edits, source):
        # TODO FIX cursor position after source update
        self.view.run_command('tk_replace_file_content', { 'file_path': path, 'source': source } )

###########################
# Reusable Sublime Commands
###########################

class TkShowStatusMessageCommand(sublime_plugin.ApplicationCommand):
    def run(self, message):
        sublime.status_message(message)

class TkOpenFileCommand(sublime_plugin.WindowCommand):
    def run(self, file_path):
        self.window.open_file(file_path, sublime.ENCODED_POSITION | sublime.FORCE_GROUP, self.window.active_group())

class TkOpenFilePreviewCommand(sublime_plugin.WindowCommand):
    def run(self, file_path):
        self.window.open_file(file_path, sublime.TRANSIENT | sublime.ENCODED_POSITION | sublime.FORCE_GROUP, self.window.active_group())

class TkOpenFileAtOffsetCommand(sublime_plugin.WindowCommand):
    def run(self, file_path, offset):
        self.window.run_command('tk_open_file', { 'file_path': file_path })
        self.window.run_command('tk_jump_to_offset', { 'offset': offset })

class TkJumpToOffsetCommand(sublime_plugin.WindowCommand):
    view = None
    offset = 0
    def run(self, offset):
        view = self.window.active_view();
        if view.is_loading(): # need to wait for file open (see TkJumpToOffsetFileOpenedEventListener)
            TkJumpToOffsetCommand.view = view
            TkJumpToOffsetCommand.offset = int(offset)
            return;

        view.sel().clear()
        view.sel().add(sublime.Region(offset))
        sublime.set_timeout(lambda: view.show_at_center(offset), 0)

class TkJumpToOffsetFileOpenedEventListener(sublime_plugin.EventListener):
    # very weird but only "on_load_async" + "set_timeout" combination works reliably for some reason :/
    def on_load_async(self,view):
        if view == TkJumpToOffsetCommand.view:
            offset = TkJumpToOffsetCommand.offset
            view.sel().clear()
            view.sel().add(sublime.Region(offset))
            sublime.set_timeout(lambda: view.show_at_center(offset), 0)
            TkJumpToOffsetCommand.file_path = ''
            TkJumpToOffsetCommand.offset = ''

class TkReplaceFileContentCommand(sublime_plugin.TextCommand):
    def run(self, edit, file_path, source):
        self.view.window().run_command('tk_open_file', { 'file_path': file_path })
        file_view = self.view.window().find_open_file(file_path)
        if file_view: # something went wrong while opening the file
            file_view.replace(edit, sublime.Region(0, file_view.size()), source)
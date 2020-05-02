import os

def find_working_dir(view):
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

import sublime

def filename():
    return 'phpactor.sublime-settings'

def get_phpactor_bin():
    return get_setting('phpactor_bin')

def get_command_setting(command_name, property, default=None):
    command_settings = get_command_settings(command_name)

    if not property in command_settings:
        return default

    return command_settings[property]

def get_command_settings(command_name):
    command_settings = get_setting('command_settings')

    if not command_settings:
        return []

    if not command_name in command_settings:
        return []

    return command_settings[command_name]

def get_setting(name, default=None):
    project_data = sublime.active_window().project_data()

    # setting in run time
    view_setting = sublime.active_window().active_view().settings().get(name, None)
    if view_setting != None:
        return view_setting

    if (project_data and 'phpactor' in project_data and name in project_data['phpactor']):
        return project_data['phpactor'][name]

    return sublime.load_settings(filename()).get(name, default)
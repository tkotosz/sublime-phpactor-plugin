import sublime

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

def get_sidebar_menu_setting(sidebar_option_name, property, default=None):
    sidebar_menu_settings = get_sidebar_menu_settings(sidebar_option_name)

    if not property in sidebar_menu_settings:
        return default

    return sidebar_menu_settings[property]

def get_sidebar_menu_settings(sidebar_option_name):
    sidebar_menu_settings = get_setting('sidebar_menu_settings')

    if not sidebar_menu_settings:
        return []

    if not sidebar_option_name in sidebar_menu_settings:
        return []

    return sidebar_menu_settings[sidebar_option_name]

def get_tab_context_menu_setting(tab_context_option_name, property, default=None):
    tab_context_menu_settings = get_tab_context_menu_settings(tab_context_option_name)

    if not property in tab_context_menu_settings:
        return default

    return tab_context_menu_settings[property]

def get_tab_context_menu_settings(tab_context_option_name):
    tab_context_menu_settings = get_setting('tab_context_menu_settings')

    if not tab_context_menu_settings:
        return []

    if not tab_context_option_name in tab_context_menu_settings:
        return []

    return tab_context_menu_settings[tab_context_option_name]

def get_context_menu_setting(context_option_name, property, default=None):
    context_menu_settings = get_context_menu_settings(context_option_name)

    if not property in context_menu_settings:
        return default

    return context_menu_settings[property]

def get_context_menu_settings(context_option_name):
    context_menu_settings = get_setting('context_menu_settings')

    if not context_menu_settings:
        return []

    if not context_option_name in context_menu_settings:
        return []

    return context_menu_settings[context_option_name]

def get_setting(name, default=None):
    # default sublime setting
    view_setting = sublime.active_window().active_view().settings().get(name, None)
    if view_setting != None:
        return view_setting

    user_settings = sublime.load_settings('Phpactor.sublime-settings').get(name)
    default_settings = sublime.load_settings('Phpactor-default.sublime-settings').get(name)
    current_settings = merge_settings(default_settings, user_settings)

    if not current_settings:
        return default

    return current_settings

def merge_settings(default_settings, user_settings):
    if not isinstance(default_settings, dict): # sublime only merges dicts incorrectly (no recursive merge)
        return user_settings

    settings = default_settings.copy()
    settings.update(user_settings)
    return settings
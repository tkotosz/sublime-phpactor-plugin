import sublime

def filename():
    return 'phpactor.sublime-settings'

def get_phpactor_bin():
    return '/home/tkotosz/Sites/phpactor/bin/phpactor' # TODO
    #return get_setting('phpactor_bin')

def get_setting(name, default=None):
    project_data = sublime.active_window().project_data()

    # setting in run time
    view_setting = sublime.active_window().active_view().settings().get(name, None)
    if view_setting != None:
        return view_setting

    if (project_data and 'phpactor' in project_data and name in project_data['phpactor']):
        return project_data['phpactor'][name]

    return sublime.load_settings(filename()).get(name, default)
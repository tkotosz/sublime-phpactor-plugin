# sublime-phpactor-plugin

## General information

Available commands in the command palette (CTRL+P):
```
[
  { "caption": "Phpactor: Status", "command": "phpactor_echo", "args": { "message": "Phpactor Status: OK" } },
  { "caption": "Phpactor: Offset Info", "command": "phpactor_offset_info" },
  { "caption": "Phpactor: Context Menu", "command": "phpactor_context_menu" },
  { "caption": "Phpactor: Navigate", "command": "phpactor_navigate" },
  { "caption": "Phpactor: Goto Definition", "command": "phpactor_goto_definition" },
  { "caption": "Phpactor: Goto Type", "command": "phpactor_goto_type" },
  { "caption": "Phpactor: Goto Implementation", "command": "phpactor_goto_implementation" },
  { "caption": "Phpactor: Find References", "command": "phpactor_references" },
  { "caption": "Phpactor: Transform", "command": "phpactor_transform" },
  { "caption": "Phpactor: Transform - Complete Constructor", "command": "phpactor_transform", "args": { "transform": "complete_constructor" } },
  { "caption": "Phpactor: Transform - Add Missing Properties", "command": "phpactor_transform", "args": { "transform": "add_missing_properties" } },
  { "caption": "Phpactor: Transform - Fix Namespace & Class Name", "command": "phpactor_transform", "args": { "transform": "fix_namespace_class_name" } },
  { "caption": "Phpactor: Transform - Implement Contracts", "command": "phpactor_transform", "args": { "transform": "implement_contracts" } },
  { "caption": "Phpactor: Generate Accessor", "command": "phpactor_generate_accessor" },
  { "caption": "Phpactor: Generate Method", "command": "phpactor_generate_method" },
  { "caption": "Phpactor: Extract Constant", "command": "phpactor_extract_constant" },
  { "caption": "Phpactor: Extract Expression", "command": "phpactor_extract_expression" },
  { "caption": "Phpactor: Extract Method", "command": "phpactor_extract_method" },
  { "caption": "Phpactor: Override Method", "command": "phpactor_override_method" },
  { "caption": "Phpactor: Change Visibility", "command": "phpactor_change_visibility" },
  { "caption": "Phpactor: Rename Variable", "command": "phpactor_rename_variable" },
  { "caption": "Phpactor: Import Class", "command": "phpactor_import_class" },
  { "caption": "Phpactor: Import Missing Classes", "command": "phpactor_import_missing_classes" },
  { "caption": "Phpactor: Copy Class", "command": "phpactor_copy_class" },
  { "caption": "Phpactor: Move Class", "command": "phpactor_move_class" },
  { "caption": "Phpactor: Class New", "command": "phpactor_class_new" },
  { "caption": "Phpactor: Class Inflect", "command": "phpactor_class_inflect" },
]
```

You can bind any of these commands to key-combination in the sublime-keymap config (Preferences > Key Bindings).
For example to show the phpactor's context menu on "alt+enter":
```
{ "keys": ["alt+enter"], "command": "phpactor_context_menu" }
```
Another example to run phpactor's goto definition on "F12":
```
{ "keys": ["f12"], "command": "phpactor_goto_definition" }
```

You can also bind commands to mouse actions in the sublime-mousemap config (not available in the menu, need to manually create a "Default (Linux).sublime-mousemap" file).
For example to run the phpactor's goto definition command on "ctrl+leftmousebuttonclick":
```
[
    {
        "button": "button1", 
        "count": 1, 
        "modifiers": ["ctrl"],
        "press_command": "drag_select",
        "command": "phpactor_goto_definition"
    }
]
```

## How to install the plugin?

Since it is not yet published in the sublime package control repository you can install it in the following way:
1. Open the Command Palette (CTRL+P) and run the "Package Control: Add Repository" command and provide this: https://github.com/tkotosz/sublime-phpactor-plugin
2. You should see a message on the status bar (bottom left corner) saying repository added successfully
3. Open the Command Palette (CTRL+P) and run the "Package Control: Install Package" command and choose sublime-phpactor-plugin (it shows up with that name since it uses the repo name by default - it will have a proper name once published in the package control repo)
4. You are done, the plugin installed

After installation:
The plugin uses /usr/local/bin/phpactor by default to find phpactor, if your phpactor is installed to a different location then you can specify the location in the package config here: `Preferences > Package Settings > Phpactor > Settings - User`: You can find the default config at `Preferences > Package Settings > Phpactor > Settings - Default`. Your user config should look like this:
```
{
    "phpactor_bin": "/absolute/path/to/bin/phpactor"
}
```
All phpactor command available in the command palette, also can be binded to keys, see readme here: https://github.com/tkotosz/sublime-phpactor-plugin

Now you are good to go but worth to note 2 things:

1. By default the "Find References" command uses git mode, but you can switch to composer mode (warning: much slower) - the later one will discover references in vendor as well. You can change the mode in the package setting like this:
```
{
    "phpactor_bin": "/absolute/path/to/bin/phpactor",
    "command_settings": {
        "references": {
            "filesystem": "git"
        }
    }
}
```
where filesystem can be "git" or "composer".

2. The goto implementation command requires indexing so if you would like to use that command then don't forget to start the phpactor indexer like this:
`bin/phpactor index:build --watch --working-dir=/absolute/path/to/your/project/dir`

## Auto-Completion

For auto-completion you can use the RPC command or you can use the Language Server implementation. Since the Language Server implementation provides way better integration then using the RPC auto-completion command I recommend to configure the Language Server.
1. Install the Sublime LSP Plugin: https://github.com/sublimelsp/LSP
2. Configure it to use Phpactor: https://phpactor.readthedocs.io/en/develop/lsp/sublime.html

On the other hand if you would like to use the RPC-based completion then it can be turned on in `Preferences > Package Settings > Phpactor > Settings - User`:
```
{
    "command_settings": {
        "complete": {
            "enabled": true
        }
    }
}
```
Note that it can offer auto-completion, but not always handled perfectly by this Plugin and I am not planning to spend to much time making any better since I will use LSP for this.

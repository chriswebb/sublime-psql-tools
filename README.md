# PostgreSQL Execute
***[Sublime Text 3+](http://www.sublimetext.com/) Package. Install via an updated version of  [Package Control 2+](https://sublime.wbond.net/installation). Just &#42;&#42;DON'T&#42;&#42; install manually.***

## Installation

1. If you don't have it already, follow the instructions on [https://sublime.wbond.net/installation](https://sublime.wbond.net/installation) to install Package Control 2+.
2. In Sublime Text, press <kbd>Ctrl+Shift+P</kbd> (Win, Linux) or <kbd>⌘⇧p</kbd> (OS X) to open the command palette.
3. Choose `Package Control: Select Repository`.
4. Choose `Package Control: Install Package`.
5. Select **PostgreSQL Execute**.

## Description 
A plugin for Sublime Text 3 that allows the execution of PSQL commands directly from the editor.

See: http://www.sublimetext.com/


## Setup
Create a Main.sublime-menu file in your Packages/User folder. Then add items for each database you would like to query.

### Add setting example

To add a new database called "my_database" to the Database menu under System Preferences:

```js
[{
    "id": "preferences",
    "children":
    [{
        "id": "package-settings",
        "children":
        [{
            "id": "psql-execute-settings",
            "children":
            [{
                "id": "psql-execute-settings-database",
                "children":
                [{
                    "caption": "my_database",
                    "command": "psql_config_set", "args": 
                    {
                        "name": "database",
                        "value": "my_database"
                    }
                }]
            }]
        }]
    }]
}]
```

then browse to Main > Preferences > Package Settings > PSQL Execute > Database and select your newly added database.

### Add new execute option with custom values example

To add a new Execute method to the non-default hostname "production.mysite" to the PostgreSQL menu under Tools:

```js
[{
    "id": "tools",
    "children":
    [{
        "id":"psql-execute-tools",
        "children":
        [{
            "caption":"Execute (Production)",
            "command":"psql_execute",
            "args": { "host": "production.mysite" }
        }]
    }]
},
{
    "id": "preferences",
    "children":
    [{
        "id": "package-settings",
        "children":
        [{
            "id": "psql-execute-settings",
            "children":
            [{
                "id": "psql-execute-settings-database",
                "children":
                [{
                    "caption": "my_database",
                    "command": "psql_config_set", "args": 
                    {
                        "name": "database",
                        "value": "my_database"
                    }
                }]
            }]
        }]
    }]
}]
```

then select your text and click Tools > PostgreSQL > Execute (Production)

## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Credits
This README template was pulled from https://gist.github.com/zenorocha/4526327
## License
MIT License. See LICENSE file.

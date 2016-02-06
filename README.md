# PSQLExecute
***[Sublime Text 3+](http://www.sublimetext.com/) Package. Install via an updated version of  [Package Control 2+](https://sublime.wbond.net/installation). Just &#42;&#42;DON'T&#42;&#42; install manually.***

## Description 
A plugin for Sublime Text 3 that allows the execution of PSQL commands directly from the editor.

See: http://www.sublimetext.com/


## Setup
Create a Main.sublime-menu file in your Packages/User folder. Then add items for each database you would like to query.

For example to connect to two postgres databases at separate ports 5432 and 6432,  create two items:

```js
[
    {
        "caption": "Tools",
        "mnemonic": "t",
        "id": "tools",
        "children":
        [
            {
                "caption": "PSQL Execute",
                "mnemonic": "f",
                "id": "psql",
                "children":
                [
                    {
                        "command": "psql_execute",
                        "args": {"host":"localhost", "port": "5432", "database": "postgres", "user":"postgres"},
                        "caption": "Postgres"
                    },
                    {
                        "command": "psql_execute",
                        "args": {"host":"localhost", "port": "6432", "database": "postgres", "user":"postgres"},
                        "caption": "Postgres 6432"
                    }
                ]
            }
        ]
    }
]
```

then browse to Tools > PSQL Execute and select the database you would like to run your query against.

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

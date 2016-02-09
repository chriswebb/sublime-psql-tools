# PostgreSQL Developer Tools

***[Sublime Text 3+](http://www.sublimetext.com/) Package. Install via an updated version of  [Package Control 2+](https://sublime.wbond.net/installation). Just &#42;&#42;DON'T&#42;&#42; install manually.***

## Installation

1. If you don't have it already, follow the instructions on [https://sublime.wbond.net/installation](https://sublime.wbond.net/installation) to install Package Control 2+.
2. In Sublime Text, press <kbd>Ctrl+Shift+P</kbd> (Win, Linux) or <kbd>⌘⇧p</kbd> (OS X) to open the command palette.
3. Choose `Package Control: Install Package`.
4. Select **PostgreSQL Developer Tools**.

## Description 

A plugin for Sublime Text that allows the execution of PostgreSQL commands directly from the editor.

See: http://www.sublimetext.com/


## Setup

Create a Main.sublime-menu file in your Packages/User folder. Then add connections for each database you would like to query.

### Add a new connection

To add a new connection to the PostgreSQL menu under Tools to host "my_host", database "my_database" with user "my_user", edit the Main.sublime-menu with the following information:

```js
[{
    "id": "tools",
    "children":
    [{
        "id":"psql-tools",
        "children":
        [{
            "id": "psql-connections",
            "children":
            [{
                "id": "my-database",
                "caption":"My Database",
                "command":"psql_conn_new",
                "args": { "database": "my_database", "host": "my_host", "user": "my_user"}
            }]
        }]
    }]
}]
```

Next click Tools > PostgreSQL > Connections > My Database

## References

Commands provided by this plugin:

- `psql` : `args` : `Settings`

        Execute PostgreSQL query with data supplied from one of the following three methods:

        - Files specified in the 'files' setting
        - Selected text of the current view
        - If no text selected, all of the text in the current view

- `psql_conn` : `args` : `Settings`

        Create new connection from current configuration settings or user supplied values.

- `psql_conn_new` : `args` : `Settings`

        Create new connection from default configuration settings or user supplied values.

- `psql_config` : `args` : `Settings`

        Update current connection configuration settings with user supplied values.

- `psql_config_set` : `args` : `{name, value}`

        Set current connection configuration settings with user supplied value.

- `psql_config_unset` : `args` : `{name}`

        Reset the current connection configuration settings back to default.

- `psql_config_clear` : 

        Reset all current connection configuration settings back to defaults.

- `psql_config_save` :

        Save the current connection configuration settings as the defaults.


### Settings

Values used when calling psql. To overwrite default values select Preferences > PostgreSQL > Settings - User. Prefix all settings with the "default_" keyword.

#### Plugin Settings 

 - `psql_path` : `/usr/bin/psql`

        Path to your desired psql executable in the file system.

 - `prompt_for_password` : `True`

        Prompt for input if password is not supplied for the connection through configuration. 
        Does not prompt if a password file exists (e.g. ~/.pgpass or passfile) or a service has been defined. 

 - `warn_on_empty_password` : `True`

        Display a warning if password is not entered after being prompted.

 - `output_to_newfile` : `False`

        Creates a new file for each file or region which runs when the psql command is called.

 - `files` : `[]`

        A list of files to run the query against. 


#### PostgreSQL Settings

PostgreSQL settings are based off of environmental variables. The list of supported settings is located [here](http://www.postgresql.org/docs/current/static/libpq-envars.html) on the [PostgreSQL Documention site](http://www.postgresql.org/docs/current/static/).

The following is a mapping of PostgreSQL environment variable names to internal settings names:

- `PGHOST`: `host` 
- `PGHOSTADDR`: `hostaddr` 
- `PGPORT`: `port` 
- `PGDATABASE`: `database`
- `PGUSER`: `user` 
- `PGPASSWORD`: `password`
- `PGPASSFILE`: `passfile` 
- `PGSERVICE`: `service` 
- `PGSERVICEFILE`: `servicefile`
- `PGREALM`: `kerberos_realm` 
- `PGOPTIONS`: `options` 
- `PGAPPNAME`: `application_name`
- `PGSSLMODE`: `sslmode` 
- `PGREQUIRESSL`: `requiressl` 
- `PGSSLCOMPRESSION`: `sslcompression`
- `PGSSLCERT`: `sslcert` 
- `PGSSLKEY`: `sslkey` 
- `PGSSLROOTCERT`: `sslrootcert` 
- `PGSSLCRL`: `sslcrl` 
- `PGREQUIREPEER`: `requirepeer` 
- `PGKRBSRVNAME`: `krbsrvname`
- `PGGSSLIB`: `gsslib` 
- `PGCONNECT_TIMEOUT`: `connect_timeout`
- `PGCLIENTENCODING`: `client_encoding` 
- `PGDATESTYLE`: `datestyle`
- `PGTZ`: `timezone` 
- `PGGEQO`: `geqo` 
- `PGSYSCONFDIR`: `sysconfdir`
- `PGLOCALEDIR`: `localedir`


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D


## Roadmap

Features planned for the future:

- Connection management
- Project style schema management
- Data manipulation
- Better support for the results
- Better error reporting

## Disclaimer

PostgreSQL is a trademark of the PostgreSQL Global Development Group. See [here](https://wiki.postgresql.org/wiki/Trademark_Policy) for more details. I am not affiliated with this group in any capacity.

## License

MIT License. See LICENSE file.

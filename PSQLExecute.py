# The MIT License (MIT)

# Copyright (c) 2016 Chris Webb

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from sublime import load_settings, status_message, ok_cancel_dialog, Region, active_window
from sublime_plugin import TextCommand
from threading import Thread, Lock
from time import time
from subprocess import Popen, PIPE, STDOUT
from os import environ
from os.path import isfile, expanduser, split
from collections import MutableMapping 
from traceback import format_exc

class PsqlExecuteSettings(MutableMapping):
    __instance = None
    __settings = None
    __defaults = {}
    __overrides = {}
    postgres_variables = { 'host':'PGHOST', 'hostaddr':'PGHOSTADDR', 'port':'PGPORT', 
                              'database':'PGDATABASE', 'user':'PGUSER', 'password':'PGPASSWORD',
                              'passfile':'PGPASSFILE', 'service':'PGSERVICE', 'servicefile':'PGSERVICEFILE',
                              'kerberos_realm':'PGREALM', 'options':'PGOPTIONS', 'appname':'PGAPPNAME',
                              'sslmode':'PGSSLMODE', 'requiressl':'PGREQUIRESSL', 'sslcompression':'PGSSLCOMPRESSION',
                              'sslcert':'PGSSLCERT', 'sslkey':'PGSSLKEY', 'sslrootcert':'PGSSLROOTCERT', 
                              'sslcrl':'PGSSLCRL', 'requirepeer':'PGREQUIREPEER', 'krbsrvname':'PGKRBSRVNAME',
                              'gsslib':'PGGSSLIB', 'connect_timeout':'PGCONNECT_TIMEOUT',
                              'client_encoding':'PGCLIENTENCODING', 'datestyle':'PGDATESTYLE',
                              'timezone':'PGTZ', 'geqo':'PGGEQO', 'sysconfdir':'PGSYSCONFDIR',
                              'localedir':'PGLOCALEDIR', 'psql_path': '', 'prompt_for_password': '', 'files': '' }

    def __new__(cls, *args, **kwargs):
        if PsqlExecuteSettings.__instance is None:
            PsqlExecuteSettings.__instance = MutableMapping.__new__(cls)

        PsqlExecuteSettings.__instance.__reload_settings(dict(*args, **kwargs))
        return PsqlExecuteSettings.__instance

    def __init__(self, *args, **kwargs):
        self.output_lock = Lock()
        self.__settings = load_settings('PSQLExecute.sublime-settings')
        self.__settings.clear_on_change('reload')
        self.__settings.add_on_change('reload', self.__reload)

    def __reload(self):
        self.__defaults = {}

    def __reload_settings(self, settings):
        self.__reload()
        self.update(settings)

    @classmethod
    def __try_validate_name(cls, name):
        return name in cls.postgres_variables

    @classmethod
    def __validate_name(cls, name):
        if not cls.__try_validate_name(name):
            raise ValueError('Argument ' + name + ' not recognized.')

    def __getitem__(self, name):
        self.__validate_name(name)
        return self.__get(self.__keytransform__(name))

    def __setitem__(self, name, value):
        self.__validate_name(name)
        self.__defaults[self.__keytransform__(name)] = value

    def __delitem__(self, name):
        self.__validate_name(name)
        del self.__defaults[self.__keytransform__(name)]

    def __iter__(self):
        return iter(self.__defaults)

    def __len__(self):
        return len(self.__defaults)

    def __contains__(self, name):
        self.__validate_name(name)
        if self.__keytransform__(name) in self.__overrides or self.__keytransform__(name) in self.__defaults:
            return True
        else:
            value = self.__settings.get('default_'+name)
            if value:
                return True
        return False

    def __keytransform__(self, name):
        return name

    def __get(self, name):
        if self.__keytransform__(name) in self.__overrides:
            return self.__overrides[name]
        elif self.__keytransform__(name) not in self.__defaults:
            value = self.__settings.get('default_'+name)
            if value:
                self.__defaults[self.__keytransform__(name)] = value
        return self.__defaults[self.__keytransform__(name)]

    @classmethod
    def set_override(cls, name, value):
        cls.__validate_name(name)
        cls.__overrides[name] = value


    @classmethod
    def unset_override(cls, name):
        cls.__validate_name(name)
        if name in cls.__overrides:
            del cls.__overrides[name]
  
class PsqlConfigSetCommand(TextCommand):  
    def description(self):
        return 'Uses {"name": name, "value": value} to override the settings used for PostgreSQL commands and prompts if either missing.'
    
    def run(self, edit, *args, **kwargs): 
        self.__edit = edit
        self.kwargs = kwargs
        self.window =  self.view.window()

        if self.window is None:
            self.window = active_window()

        if 'name' not in self.kwargs:
            self.window.show_input_panel('Enter PostgreSQL configuration variable name:', '', self.__set_name, None, self.__cancelled)
        else:
            self.__set_name(self.kwargs['name'])

    def __cancelled(self):
        status_message('PostgreSQL configuration variable setting cancelled.')

    def __set_override(self, value):
        PsqlExecuteSettings.set_override(self.config_name, value)
        status_message('PostgreSQL configuration variable \'' + self.config_name + '\' set.')

    def __set_name(self, name):
        self.config_name = name

        if 'value' not in self.kwargs:
            self.window.show_input_panel('Enter ' + self.config_name + ':', '', self.__set_override, None, self.__cancelled)
        else:
            self.__set_override(self.kwargs['value'])

class PsqlConfigUnsetCommand(TextCommand):  
    def description(self):
        return 'Uses {"name": name} to override the settings used for PostgreSQL commands and prompts if missing.'
    
    def run(self, edit, *args, **kwargs): 
        self.__edit = edit
        self.window =  self.view.window()

        if self.window is None:
            self.window = active_window()
        if 'name' not in kwargs:
            self.window.show_input_panel('Enter PostgreSQL configuration variable name:', '', self.__set_name, None, self.__cancelled)
        else:
            self.__set_name(kwargs['name'])

    def __cancelled(self):
        status_message('PostgreSQL configuration variable unsetting cancelled.')

    def __set_name(self, name):
        self.config_name = name
        PsqlExecuteSettings.unset_override(self.config_name)
        status_message('PostgreSQL configuration variable \'' + self.config_name + '\' unset.')

  
class PsqlExecuteCommand(TextCommand):  
    def description(self):
        return 'Executes PostgreSQL commands directly from the editor'

    def run(self, edit, *args, **kwargs):  
        self.edit = edit
        self.settings = PsqlExecuteSettings(kwargs)
        self.encoding = self.view.encoding()
        self.window =  self.view.window()

        if self.window is None:
            self.window = active_window()
        if self.encoding == 'Undefined':
            self.encoding = 'UTF-8'

        password = None
        if 'password' in self.settings:
            password = self.settings['password']
        elif self.__is_password_required():
            status_message('Enter password for PostgreSQL database.')
            self.window.show_input_panel('Enter password:', '', self.__run_with_password, None, self.__cancelled)
            return
        self.__run_with_password(password)

    def __cancelled(self):
        self.__run_with_password(None)

    def __is_password_required(self):
        return 'prompt_for_password' in self.settings and self.settings['prompt_for_password'] and 'passfile' not in self.settings and 'service' not in self.settings and not isfile(expanduser('~/.pgpass'))

    def __run_with_password(self, password):
        if not password and self.__is_password_required():
            if not ok_cancel_dialog('Proceed with empty password?', 'Proceed'):
                status_message('PostgreSQL query cancelled.')
                return
        elif 'password' not in self.settings:
            self.settings['password'] = password

        self.output_panel = self.window.create_output_panel('psql_execute')
        self.output_panel.set_scratch(True)
        self.output_panel.run_command('erase_view')
        self.output_panel.set_encoding(self.encoding)

        status_message('PostgreSQL query executing...')
        thread_infos = []
        thread_num = 0

        if 'files' in self.settings:
            for fileobj in self.settings['files']:  
                if isfile(fileobj):
                    thread_num += 1
                    thread = self.__PostgresQueryExecute(self, file=fileobj)
                    thread_infos.append({'thread': thread, 'file': fileobj})

        else:
            noSelections = True
            for sel in self.view.sel():  
                if not sel.empty():
                    thread_num += 1
                    noSelections = False
                    # Get the selected text  
                    query = self.view.substr(sel)
                    thread = self.__PostgresQueryExecute(self, query=query)
                    thread_infos.append({"thread": thread, "thread_num": thread_num})

            if noSelections:
                thread_num += 1
                # Get all the text  
                query = self.view.substr(Region(0, self.view.size()))
                thread = self.__PostgresQueryExecute(self, query=query)
                thread_infos.append({"thread": thread, "thread_num": thread_num})

        for thread_info in thread_infos:
            thread_info['start_time'] = time()
            thread_info['thread'].start()

        self.__PostgresQueryHandleExecution.execute(thread_infos, thread_num)

    class __PostgresQueryHandleExecution(Thread):
        def __init__(self, thread_infos, thread_total):
            self.thread_infos = thread_infos
            self.thread_total = thread_total
            Thread.__init__(self)

        def run(self):
            new_thread_infos = []
            for thread_info in self.thread_infos:
                if thread_info['thread'].is_alive():
                    new_thread_infos.append(thread_info)
                    continue
                else:
                    completion_time = (time() - thread_info['start_time']) * 1000
                    if 'file' in thread_info:
                        dirpath, filename = split(thread_info['file'])
                        query_id = ('file ' + filename)
                    else:
                        query_id = ('query '+ thread_info['thread_num'] + '/' + self.thread_total) if thread_info['thread_num'] != 1 and self.thread_total != 1 else 'query '
                    status_message('PostgreSQL ' + query_id + ' completed in '+ str(completion_time) +' ms.')

            if len(new_thread_infos) > 0:
                self.execute(new_thread_infos, self.thread_total)

        @classmethod
        def execute(cls, thread_infos, thread_total):
            thread = cls(thread_infos, thread_total)
            thread.start()

    class __PostgresQueryExecute(Thread):
        def __init__(self, parent, query=None, file=None):
            self.parent = parent
            self.query = query
            self.file = file
            Thread.__init__(self)

        def __get_parameter(self, name, default=False):
            if name not in self.parent.settings and default:
                self.parent.settings[name] = default
            return self.parent.settings[name] if default or name in self.parent.settings else False


        def __try_add_parameter_name_to_environment(self, env, name, argname, default=False):
            value = self.__get_parameter(name, default)

            if value:
                env[argname] = value
                return True
            return False


        def run(self):
            errored = False

            try:
                cmd = [self.__get_parameter('psql_path', '/usr/bin/psql'), '--no-password'] 
                environment = environ.copy()

                for name in self.parent.settings.postgres_variables:
                    if name in self.parent.settings and self.parent.settings[name]:
                        self.__try_add_parameter_name_to_environment(environment, name, self.parent.settings.postgres_variables[name])

                client_encoding_name = self.parent.settings.postgres_variables['client_encoding']
                if client_encoding_name not in environment:
                    environment[client_encoding_name] = self.parent.encoding

                
                if (self.file): 
                    with open(self.file) as inputfile:
                        psqlprocess = Popen(cmd, stdin=inputfile, stdout=PIPE, stderr=STDOUT, env=environment)
                        stdout, stderr = psqlprocess.communicate()
                else:
                    psqlprocess = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, env=environment)
                    stdout, stderr = psqlprocess.communicate(bytes(self.query, self.parent.encoding))

                output_text = stdout.decode(self.parent.encoding)
                retcode = psqlprocess.poll()

                if retcode == 3:
                    print('Script error Return code: ' + str(retcode))
                if retcode == 0:
                    print('Script success Return code: ' + str(retcode))
                if retcode == 1:
                    print('Script fatal client error Return code: ' + str(retcode))
                if retcode == 2:
                    print('Script fatal server error Return code: ' + str(retcode))

            except BaseException as e:
                errored = True
                output_text = format_exc()
                status_message('PostgreSQL query errored.')

            self.parent.settings.output_lock.acquire()
            self.parent.output_panel.run_command('append', {'characters': output_text})
            self.parent.window.run_command('show_panel', {'panel': 'output.psql_execute'})
            self.parent.settings.output_lock.release()

        

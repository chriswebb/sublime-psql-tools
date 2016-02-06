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

import sublime, sublime_plugin, threading
from time import time
from subprocess import Popen, PIPE, STDOUT

class PsqlExecuteSettings(object):
    __instance = None
    def __new__(cls):
        if PsqlExecuteSettings.__instance is None:
            PsqlExecuteSettings.__instance = object.__new__(cls)
        return PsqlExecuteSettings.__instance
    def __init__(self):
        self.settings = sublime.load_settings('PSQLExecute.sublime-settings')
        self.settings.clear_on_change('reload')
        self.settings.add_on_change('reload', lambda:PsqlExecuteSettings.__load)
        self.__load()
    def __load(self):
        self.psql_path = self.settings.get('psql_path', '/usr/bin/psql')
        self.host = self.settings.get('default_host')
        self.port = self.settings.get('default_port')
        self.database = self.settings.get('default_database', 'postgres')
        self.user = self.settings.get('default_user', 'postgres')
  
class PsqlExecuteCommand(sublime_plugin.TextCommand):  
    def run(self, edit, **kwargs):  
        outputPanel = self.view.window().create_output_panel('psql')
        outputPanel.set_scratch(True)
        outputPanel.run_command('erase_view')
        encoding = self.view.encoding()
        if encoding == 'Undefined':
            encoding = 'UTF-8'
        outputPanel.set_encoding(encoding)
        self.view.window().run_command('show_panel', {'panel': 'output.psql'})
        threads = []
        lock = threading.Lock()
        for sel in self.view.sel():  
            if not sel.empty():
                # Get the selected text  
                query = self.view.substr(sel)
                thread = PostgresQueryExecute(query, encoding, outputPanel, 60, lock, kwargs)
                threads.append(thread)
                thread.start()

class PostgresQueryExecute(threading.Thread):
    def __init__(self, query, encoding, outputPanel, timeout, outputLock, args):
        self.query = query
        self.encoding = encoding
        self.timeout = timeout
        self.outputPanel = outputPanel
        self.outputLock = outputLock
        self.args = args
        threading.Thread.__init__(self)
 
    def run(self):
        startTime = time()

        try:
            default = PsqlExecuteSettings()
            cmd = [default.psql_path]

            if ('host' in self.args) or (default.host):
                cmd = cmd + ['-h', self.args['host'] if 'host' in self.args else default.host]
            if ('port' in self.args) or (default.port): 
                cmd = cmd + ['-p', self.args['port'] if 'port' in self.args else default.port]
            if ('database' in self.args) or (default.database): 
                cmd = cmd + ['-d', self.args['database'] if 'database' in self.args else default.database]
            if ('user' in self.args) or (default.user): 
                cmd = cmd + ['-U', self.args['user'] if 'user' in self.args else default.user]

            self.outputLock.acquire()

            psqlProcess = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
            stdout, stderr = psqlProcess.communicate(bytes(self.query, self.encoding))

            retcode = psqlProcess.poll()
            outputText = stdout.decode(self.encoding)
            completionTime = (time() - startTime) * 1000
            outputText = outputText + 'Completed in: '+ str(completionTime) +' ms\n'

        except OSError as e:
            outputText = '%s: error occurred while invoking psql: %s' % (__name__, str(e))
        except ValueError as e:
            outputText = '%s: error occurred while creating psql command: %s' % (__name__, str(e))
 
        self.outputPanel.run_command('append', {'characters': outputText})
        self.outputLock.release()

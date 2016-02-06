import sublime, sublime_plugin, threading
from time import time
from subprocess import Popen, PIPE, STDOUT
  
class PsqlExecuteCommand(sublime_plugin.TextCommand):  
    def run(self, edit, **kwargs):  
        outputPanel = self.view.window().create_output_panel('psql')
        outputPanel.set_scratch(True)
        outputPanel.run_command('erase_view')
        self.view.window().run_command('show_panel', {'panel': 'output.psql'})
        threads = []
        lock = threading.Lock()
        for sel in self.view.sel():  
            if not sel.empty():
                # Get the selected text  
                input = self.view.substr(sel)
                thread = PostgresQueryExecute(input, outputPanel, 60, lock, kwargs)
                threads.append(thread)
                thread.start()



class PostgresQueryExecute(threading.Thread):
    def __init__(self, input, output, timeout, outputLock, args):
        self.input = input
        self.timeout = timeout
        self.output = output
        self.outputLock = outputLock
        self.args = args
        threading.Thread.__init__(self)
 
    def run(self):
        start_time = time()

        try:
            cmd = ['/usr/local/bin/psql']

            if 'host' in self.args:
                cmd = cmd + ['-h', self.args['host']]
            if 'port' in self.args: 
                cmd = cmd + ['-p', self.args['port']]
            if 'database' in self.args: 
                cmd = cmd + ['-d', self.args['database']]
            if 'user' in self.args: 
                cmd = cmd + ['-U', self.args['user']]

            self.outputLock.acquire()

            psqlProcess = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
            stdout, stderr = psqlProcess.communicate(bytes(self.input, 'UTF-8'))

            retcode = psqlProcess.poll()
            output = stdout.decode('UTF-8')

        except OSError as e:
            output = '%s: error occurred while invoking psql %s' % (__name__, str(e.strerror))
        except ValueError as e:
            output = '%s: error occurred while creating psql command %s' % (__name__, str(e))
 
        completionTime = (time() - start_time) * 1000
        output = output + 'Completed in: '+ str(completionTime) +' ms\n'
        self.output.run_command('append', {'characters': output})
        self.outputLock.release()


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

from .psql import PsqlBaseWindowCommand, set_status

class PsqlConfigUnsetCommand(PsqlBaseWindowCommand):  
    def description(self):
        return 'Uses {"name": name} to unset the user-specified settings used for PostgreSQL commands. It prompts if the argument is missing.'
    
    def run(self, edit, *args, **kwargs): 
        if 'name' not in kwargs:
            self.window.show_input_panel('Enter PostgreSQL configuration variable name:', '', self.__set_name, None, self.__cancelled)
        else:
            self.__set_name(kwargs['name'])

    def __cancelled(self):
        set_status('PostgreSQL configuration variable unsetting cancelled.')

    def __set_name(self, name):
        self.config_name = name
        self.settings.unset_user_specified(self.config_name)
        set_status('PostgreSQL configuration variable \'' + self.config_name + '\' unset.')
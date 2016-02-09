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

class PsqlConfigSetCommand(PsqlBaseWindowCommand):  
    def description(self):
        return 'Uses {"name": name, "value": value} to set the user-specified settings used for PostgreSQL commands. It prompts if either argument is missing.'
    
    def run(self, edit, *args, **kwargs): 
        self.__edit = edit
        self.kwargs = kwargs

        if 'name' not in self.kwargs:
            self.window.show_input_panel('Enter PostgreSQL configuration variable name:', '', self.__set_name, None, self.__cancelled)
        else:
            self.__set_name(self.kwargs['name'])

    def __cancelled(self):
        set_status('PostgreSQL configuration variable setting cancelled.')

    def __set_user_specified(self, value):
        self.settings.set_user_specified(self.config_name, value)
        set_status('PostgreSQL configuration variable \'' + self.config_name + '\' set.')

    def __set_name(self, name):
        self.config_name = name

        if 'value' not in self.kwargs:
            self.window.show_input_panel('Enter ' + self.config_name + ':', '', self.__set_user_specified, None, self.__cancelled)
        else:
            self.__set_user_specified(self.kwargs['value'])
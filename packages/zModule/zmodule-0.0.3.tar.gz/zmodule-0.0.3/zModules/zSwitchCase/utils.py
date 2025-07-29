
#! switchcase.py

class _SwitchCase:

    def __init__(self):

        self.is_value = None

    def switch(self, value):

        self.is_value = value

    def case(self, compare_value, function):

        if self.is_value == compare_value:

            function()
    
SwitchCase = _SwitchCase()

def switch(value):

    SwitchCase.switch(value)

def case(compare_value, function):

    SwitchCase.case(compare_value, function)
   
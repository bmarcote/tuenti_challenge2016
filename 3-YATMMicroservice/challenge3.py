import sys
from numpy import maximum
from collections import defaultdict

class Tape:
    def __init__(self, code):
        self._code = list(code)
        self._pointer = 0
        self.state = 'start'

    def write(self, char):
        self._code[self._pointer] = char

    def move(self, direction):
        if direction == 'left':
            self._pointer -= 1
            if self._pointer < 0:
               self._code = ['']+self._code
               self._pointer += 1
        elif direction == 'right':
            self._pointer += 1
            if self._pointer >= len(self._code):
                self._code += [' ']
    
    def read_trigger(self):
        return self._code[self._pointer]
    
    def code(self):
        return ''.join(self._code)



class Actions:
    def __init__(self):
        """actions must be a dict with all the actions to execute
        ordering is a list with the name of the actions (as they appear
        in the keys of the actions dict with the order in which they
        must be applied.
        The only accepted actions: write, move, [state]
        """
        self._actions = {}
        self._ordering = []

    def add_action(self, new_action_key, new_action_value):
        """Add an action to Action that was not defined during the init."""
        self._actions[new_action_key] = new_action_value
        self._ordering += [new_action_key]
    
    def do_actions(self, tape):
        for next_action in self._ordering:
            if next_action == 'write':
                tape.write(self._actions[next_action])
            elif next_action == 'move':
                tape.move(self._actions[next_action])
            elif next_action == 'state':
                tape.state = self._actions[next_action]


class State:
    def __init__(self, name):
        self.name = name
        self._triggers = {}
    
    def set_new_trigger(self, new_trigger):
        self._triggers[new_trigger] = Actions()
    
    def add_new_action(self, trigger, new_action_key, new_action_value):
        self._triggers[trigger].add_action(new_action_key, new_action_value)

    def do_actions_for_trigger(self, trigger, tape):
        self._triggers[trigger].do_actions(tape)


def count_leadingspaces(text):
    counter = 0
    pos = 0
    while True: # it can fail.. but not in this problem
        if text[pos] == ' ':
            counter += 1
            pos += 1
        else:
            return counter


def process_tape(a_tape):
    tape = Tape(a_tape)
    while tape.state != 'end':
        this_trigger = tape.read_trigger()
        states[tape.state].do_actions_for_trigger(this_trigger, tape)

    return tape.code()


path = open(sys.argv[1], 'r')
output = open(sys.argv[2], 'w')


is_code = False
is_tapes = False

states = {}
current_state = None
current_trigger = None

lines = path.readlines()
# Obtains the indentation of each line
for a_line in lines:
    a_line = a_line.replace('\n', '')
    indent = count_leadingspaces(a_line)
    if indent == 0:
        # We change from code or tapes or it is just ---
        if a_line == 'code:':
            is_code = True
        elif a_line == 'tapes:':
            is_tapes = True
            is_code = False
    
    elif is_tapes:
        n_tape, content = [qq.strip().replace("'", '') for qq in a_line.split(':')]
        result = process_tape(content)
        output.write('Tape #{}: {}\n'.format(n_tape, result))

    else: # is code (actually I do not need the is_code..)
        if indent == 2:
            # it is a new state
            states[a_line.lstrip()[:-1]] = State(a_line.lstrip()[:-1])
            current_state = a_line.lstrip()[:-1]
        elif indent == 4:
            # It is a new trigger
            states[current_state].set_new_trigger(a_line.lstrip()[:-1].replace("'", ''))
            current_trigger = a_line.lstrip()[:-1].replace("'", '')
        elif indent == 6:
            # It is a new action
            a_line.lstrip()
            a_key, a_value = [qq.strip() for qq in a_line.split(':')]
            states[current_state].add_new_action(current_trigger, a_key, a_value.replace("'", ''))
            # There will be only ' if the action is write. Otherwise, the replace will do nothing


path.close()
output.close()

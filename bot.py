import random
import json


def distance(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n, m)) space
        a, b = b, a
        n, m = m, n

    # Keep current and previous row, not entire matrix
    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + \
                1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


# TODO: Add quick responses for user (readable from json)

def secure_message(message):
    return message

class State():
    name = None
    unknown = None
    reactions = []
    raw_func = False

    def __init__(self, master, name, unknown=None):
        self.master = master
        self.name = name
        self.reactions = []
        self.unknown = None
        self.raw_func = None
        self.israw = False
        self.set_unknown(unknown)
        master.set_state(self, name)

    def set_unknown(self, phrase):
        if type(phrase) == list:
            self.unknown = tuple(phrase)
        elif type(phrase) == tuple:
            self.unknown = phrase
        else:
            try:
                self.unknown = str(phrase)
            except Exception():
                self.unknown = None

    def _add_reaction(self, reaction):
        self.reactions.append(reaction)

    def _set_raw_action(self, action):
        self.israw = True
        self.raw_func = action

    # TODO Add userobj
    def process(self, user, message):
        new_state = False

        # If state accepts raw input, we need to parse it.
        if self.israw:
            new_state = self.raw_func(user, message)
        # Or if the user is provided with options, iterate through them.
        else:
            for reaction in self.reactions:
                if reaction.match(message):

                    # FIXME right now state name is returning from the function.
                    # Something should be done with it.

                    new_state = reaction.act(user, message)
                    break

        return new_state

class Reaction():
    action = None

    def __init__(self, action, keywords):
        self.action = action
        self.keywords = tuple(a.lower() for a in keywords)

    def match(self, text):

        # This algorythm checks if there are any
        # acceptable keywords. It can be upgraded to ignore
        # typos and other things like that.
        # TODO: Upgrade match function
        for keyword in self.keywords:
            print(f"{keyword}: {distance(keyword, text.lower())/len(text.lower())}")
            if distance(keyword, text.lower()) / len(text.lower()) < 0.30:
                return keyword
        return False

    def act(self, user, message):
        if self.action:
            return self.action(user, message)
        else:
            return None

    def set_action(self, action):
        if type(action) == Reaction:
            self.action = action
        else:
            raise TypeError

class Speech():
    states = {}
    startstate = None
    greet_func = None

    def __init__(self, start=None, unknown=None, welcome=None):
        self.states = {}
        self.startstate = start
        self.unknown = unknown
        self.welcome = welcome
        self.greet_func = None

    def set_state(self, state, name):
        if type(state) == State and type(name) == str:
            self.states[name] = state
        else:
            raise TypeError('Either name or state is incorrect type.')

    # TODO Make messages secure.
    def process(self, user, message): 

        message = secure_message(message)

        if not user.get_state():
            user.set_state(self.startstate)
            if self.greet_func:
                self.greet_func(user, message)
        cur_state = self.states[user.get_state()]
        response = cur_state.process(user, message)
        if not response:
            if cur_state.unknown:
                unknown = cur_state.unknown
            elif self.unknown:
                unknown = self.unknown
            else:
                return None

            if type(unknown) == tuple:
                return random.choice(unknown)
            elif type(unknown) == str:
                return unknown

        else:
            user.set_state(response)

    def read_states_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)['states']
        for key in data:
            state = State(self, key)
            unknown = data[key].get('unknown')
            starter = data[key].get('start', False)
            if starter:
                self.startstate = key
            if unknown:
                state.set_unknown(unknown)
        if not self.startstate:
            raise Exception("No starting state!")
    
    def greeting(self):
        def info(f):
            self.greet_func = f
        return info

    def reaction(self, statename, keywords):
        def info(f):
            state = self.states[statename]
            state._add_reaction(Reaction(f, keywords))
        return info

    def raw(self, statename):
        def info(f):
            state = self.states[statename]
            state._set_raw_action(f)
        return info






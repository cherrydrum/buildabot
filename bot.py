

class Speech():
    states = {}
    current_state = None
    temp_data = {}

    def __init__(self, start):
        self.states = {}
        self.current_state = start

    def process(self, message):
        cur_state = self.states[self.current_state]
        response = cur_state.process(message)
        if not response:

            #FIXME I need to add interface for unknown reaction.
            #TODO Check if state is present in speech
            print (cur_state.unknown)
        else:
            self.current_state = response

    def reaction(self, state, keywords):
        def info(f):
            a = State(state)
            self.states[state] = a
            a._add_reaction(Reaction(f, keywords))

        return info


# TODO: Make pre-word and after-word, just in case.
# TODO: Also some states can wait just for raw input, so
#       no reactions are needed.
class State():
    name = None
    unknown = None
    reactions = []

    def __init__(self, name):
        self.name = name
        self.reactions = []
        self.unknown = None

    def set_unknown(self, phrase):
        self.unknown = phrase
    
    def _add_reaction(self, reaction):
        self.reactions.append(reaction)

    def remove_reaction(self, reaction):
        self.reactions.remove(reaction)

    def process(self, message):
        for reaction in self.reactions:
            if reaction.match(message):

                # FIXME right now state name is returning from the function.
                # Something should be done with it.

                new_state = reaction.act(message)
                return new_state

        # If there is no matching keywords, we should
        # probably just return False, BUT!!!
        # What about raw input? It also should be checked
        # and processed.

        return False


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
            if keyword == text.lower():
                return True
        return False

    def act(self, message):
        if self.action:
            return self.action(message)
        else:
            return None

    def set_action():
        self.action = action

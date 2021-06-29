from app.register import register_instance
from app import log

INIT="INIT"
NORMAL="NORMAL"

@register_instance
class State:

    def __init__(self, states):
        log.info("State object initialized")
        self.states = states
        self.state = INIT

    def __getattr__(self, name: str):
        try:
            return super().__getattr__(self, name)
        except AttributeError:
            ...
        
        log.info(f"Switching to state {name.upper()}")
        if name.upper() in self.states:
            self.state = name.upper()            

    def current(self):
        return self.state

    def is_(self, state):
        return state.upper() == self.state

from app.register import register_instance
from app import log

INIT = "INIT"
NORMAL = "NORMAL"


@register_instance
class State:
    def __init__(self, states):
        log.info("State object initialized")

        assert isinstance(states, list)
        assert len(states) > 0

        self.states = states
        self.state = INIT

    def __getattr__(self, name: str):
        try:
            return super().__getattr__(self, name)
        except AttributeError:
            ...

        assert isinstance(name, str)
        log.info(f"Switching to state {name.upper()}")
        if name.upper() in self.states:
            self.state = name.upper()
        else:
            raise AttributeError(f"No state: {name.upper()}")

    def current(self):
        return self.state

    def is_(self, state):
        return state.upper() == self.state

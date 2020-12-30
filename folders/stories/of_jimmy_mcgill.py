from folders.register import Register as __
from folders.signal_bus import signal_bus


class HowToCopyAMessage:
    def copy(self, message):
        __.Jimmy.send(message)


signal_bus.subscribe("copy", HowToCopyAMessage())

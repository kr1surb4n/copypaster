from copypaster.register import Register as __
from copypaster.signal_bus import signal_bus


class HowToCopyAMessage:
    def on_copy(self, message):
        __.Jimmy.send(message)


signal_bus.subscribe('copy', HowToCopyAMessage())

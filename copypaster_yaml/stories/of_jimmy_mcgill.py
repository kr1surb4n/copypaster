from app.register import Register as __
from app.signal_bus import subscribe


@subscribe
def copy(message):
    __.Jimmy.send(message)

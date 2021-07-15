from app.register import Register as __
from app.signal_bus import subscribe
from copypaster import log


@subscribe
def copy(message):
    log.info(f"Copy: {message}")
    __.Jimmy.send(message)

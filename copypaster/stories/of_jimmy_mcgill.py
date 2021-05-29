from app.register import Register as __
from app.signal_bus import subscribe


@subscribe
def copy(message):
    __.Jimmy.send(message)

@subscribe
def autosave_on():
    __.AppState["app"] = State.AUTOSAVE

@subscribe
def autosave_off():
    __.AppState["app"] = State.NORMAL

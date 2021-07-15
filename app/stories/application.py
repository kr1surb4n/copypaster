from app.register import Register as __
from app.signal_bus import subscribe, emit, event
from app import log


@subscribe
def activate_app():
    log.info(f"State is {__.State.current()}")
    log.info("All green. Welcome to application.")


@subscribe
def start_app():
    __.State.normal
    emit(event.load_styles)


@subscribe
def quit(*args, **kwargs):
    __.Application.handle_quit('action', 'param')


@subscribe
def load_styles():
    __.Style.load_styles()


@subscribe
def reset_styles(*args):
    __.Style.reset_styles()

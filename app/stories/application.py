from app.register import Register as __
from app.signal_bus import subscribe, emit, event
from app import log

@subscribe
def activate_app():
    log.info(f"State is {__.State.current()}")
    log.info("All green. Welcome to application.")

@subscribe
def start_app():
    print(__.State)
    __.State.normal()
    #emit(event.load_default_styles)
    ...


@subscribe
def quit(*args, **kwargs):
    __.Application.handle_quit('action', 'param')


@subscribe
def reload_css(*args):
    emit(event.reload_default_styles)


def test_application_stories():
    raise NotImplementedError("Tests for application stories are missing")

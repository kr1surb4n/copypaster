from app.register import Register as __
from app.signal_bus import subscribe, emit
from app.widgets.dialogs import DialogError


@subscribe
def start_app():
    emit('load_default_styles')


@subscribe
def quit(*args, **kwargs):
    pass


@subscribe
def error_show_dialog(message):
    dialog = DialogError(__.Application.win, message)
    dialog.run()
    dialog.hide()


@subscribe
def about_button(*args):
    pass


@subscribe
def reload_css(*args):
    emit('reload_default_styles')


@subscribe
def on_quit_app(*args):
    __.Application.handle_quit('action', 'param')


@subscribe
def quit_app(*args):
    __.Application.handle_quit('action', 'param')


def test_application_stories():
    raise NotImplementedError("Tests for application stories are missing")

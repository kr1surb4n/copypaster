from app.register import Register as __
from app.signal_bus import subscribe, emit, signals
from app.widgets.dialogs import DialogError


@subscribe
def start_app():
    emit(signals.load_default_styles)


@subscribe
def quit(*args, **kwargs):
    pass


@subscribe
def error_show_dialog(message):
    dialog = DialogError(__.Application.win, message)
    dialog.run()
    dialog.destroy()

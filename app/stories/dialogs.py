from app.signal_bus import subscribe


@subscribe
def error_show_dialog(message):
    ...


@subscribe
def about_button(*args):
    ...

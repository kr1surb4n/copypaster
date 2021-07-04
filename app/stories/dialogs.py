from app.signal_bus import subscribe


@subscribe
def error_show_dialog(message):
    ...


@subscribe
def about_button(*args):
    ...


def test_dialog_stories():
    raise NotImplementedError("Tests for dialog stories are missing")

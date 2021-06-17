from app.register import Register as __
from app.signal_bus import subscribe
from app.widgets.dialogs import DialogError


@subscribe
def error_show_dialog(message):
    dialog = DialogError(__.Application.win, message)
    dialog.run()
    dialog.hide()


def test_dialog_stories():
    raise NotImplementedError("Tests for dialog stories are missing")

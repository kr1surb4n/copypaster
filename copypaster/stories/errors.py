from app.register import Register as __
from app.signal_bus import signal_bus, subscribe
from copypaster.widgets.dialogs import DialogError



@subscribe
def error_show_dialog(message):
    dialog = DialogError(__.Application.win, message)
    dialog.run()
    dialog.destroy()
from folders.register import Register as __
from folders.signal_bus import signal_bus
from folders.widgets.dialogs import DialogError


class DisplayErrorDialog:
    def error_show_dialog(self, message):
        dialog = DialogError(__.Application.win, message)
        dialog.run()
        dialog.destroy()


signal_bus.subscribe("error_show_dialog", DisplayErrorDialog())

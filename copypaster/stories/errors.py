from copypaster.register import Register as __
from copypaster.signal_bus import signal_bus
from copypaster.widgets.dialogs import DialogError


class DisplayErrorDialog:
    def on_error_show_dialog(self, message):
        dialog = DialogError(
            __.Application.win, message)
        dialog.run()
        dialog.destroy()


signal_bus.subscribe('error_show_dialog', DisplayErrorDialog())

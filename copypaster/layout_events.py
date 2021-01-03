from copypaster.register import Register as __
from copypaster.signal_bus import signal_bus
from copypaster import log, State, AppState

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa


class ToggleButtons:
    autosave = 'autosave'
    edit = 'edit'
    remove = 'remove'

    def names(self):
        return [ToggleButtons.autosave, ToggleButtons.edit, ToggleButtons.remove]


class LayoutEvents:
    def __init__(self):
        self.clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.handle = None
        self.buttons = ToggleButtons()

    def auto_clipboard(self, clipboard, parameter):
        if AppState["app"] != State.AUTOSAVE:
            return False

        name = value = clipboard.wait_for_text()

        if not value:
            log.error("No value to save - aborting")
            return False
        signal_bus.emit("add_button", name, value)

    # menu
    def want_new_notebook(self, button):
        log.debug("Emitting new_notebook...")
        signal_bus.emit('new_notebook')

    def want_open_notebook(self, button):
        log.debug("Emitting open_notebook...")
        signal_bus.emit('open_notebook')

    def want_save_notebook(self, button):
        log.debug("Emitting save_notebook...")
        signal_bus.emit('save_notebook')

    def want_saveas_notebook(self, button):
        log.debug("Emitting save_notebook_as...")
        signal_bus.emit('save_notebook_as')

    def on_quit_app(self, *args):
        __.Application.handle_quit('action', 'param')

    def quit(self, *args):
        self.on_quit_app(*args)

    # toolbar
    def _deactive_rest_buttons(self, leave_alone):
        builder = __.Builder
        [
            builder.get_object(name).set_active(False)
            for name in self.buttons.names()
            if name != leave_alone and builder.get_object(name).get_active()
        ]

    def autosave_on(self, button):
        self._deactive_rest_buttons(ToggleButtons.autosave)

        if button.get_active():
            AppState["app"] = State.AUTOSAVE
            signal_bus.emit("autosave_on")

            self.handle = self.clip.connect("owner-change", self.auto_clipboard)
            log.debug("Autosave on")
        else:
            signal_bus.emit("autosave_off")
            AppState["app"] = State.NORMAL
            self.clip.disconnect(self.handle)
            log.debug("Autosave off")

    def edit_on(self, button):
        self._deactive_rest_buttons(ToggleButtons.edit)

        if button.get_active():
            AppState["app"] = State.EDIT
            log.debug("Edit on")
        else:
            AppState["app"] = State.NORMAL
            log.debug("Edit off")

    def remove_on(self, button):
        self._deactive_rest_buttons(ToggleButtons.remove)

        if button.get_active():
            AppState["app"] = State.REMOVE
            log.debug("Remove on")

        else:
            AppState["app"] = State.NORMAL
            log.debug("Remove off")

    def add(self, button):
        log.debug("Begin adding button")
        signal_bus.emit("open_add_button_dialog")

    def remove_notebook(self, button, name):
        pass


Layout_events = LayoutEvents()

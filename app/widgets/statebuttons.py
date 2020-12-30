from copypaster.register import register_instance
from copypaster.signal_bus import signal_bus
from copypaster import log, State, AppState

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa

# translate = {
#     "Autosave": AUTOSAVE,
#     "Edit":     `EDIT, NORMAL, REMOVE
# }


class StateButtonsCallbacks:
    def on_autosave(self, button, name):
        self._deactive_rest_buttons("autosave")

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

    def on_edit(self, button, name):
        self._deactive_rest_buttons("edit")

        if button.get_active():
            AppState["app"] = State.EDIT
            log.debug("Edit on")
        else:
            AppState["app"] = State.NORMAL
            log.debug("Edit off")

    def on_add(self, button):
        log.debug("Begin adding button")
        signal_bus.emit("open_add_button_dialog")

    def on_remove(self, button, name):
        self._deactive_rest_buttons("remove")

        if button.get_active():
            AppState["app"] = State.REMOVE
            log.debug("Remove on")

        else:
            AppState["app"] = State.NORMAL
            log.debug("Remove off")

    def auto_clipboard(self, clipboard, parameter):
        if AppState["app"] != State.AUTOSAVE:
            return False

        name = value = clipboard.wait_for_text()

        if not value:
            log.error("No value to save - aborting")
            return False
        signal_bus.emit("add_button", name, value)

    def _deactive_rest_buttons(self, leave_alone):
        [
            button.set_active(False)
            for name, button in self.buttons.items()
            if name != leave_alone and button.get_active()
        ]


@register_instance
class StateButtons(StateButtonsCallbacks, Gtk.HBox):
    """Autosave, Edit, Remove"""

    def __init__(self):
        Gtk.Box.__init__(self, spacing=6, expand=False, vexpand=False)
        self.buttons = {}

        self.clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.handle = None

        self._create_button("Autosave", self.on_autosave, "1")
        self._create_button("Edit", self.on_edit, "2")
        self._create_button("Remove", self.on_remove, "3")

        button = Gtk.Button("Add")
        button.connect("clicked", self.on_add)
        self.pack_start(button, False, False, 0)

    def _create_button(self, name, callback, ind):
        _button = Gtk.ToggleButton(name)
        _button.connect("toggled", callback, ind)

        self.pack_start(_button, False, False, 0)

        self.buttons[name.lower()] = _button

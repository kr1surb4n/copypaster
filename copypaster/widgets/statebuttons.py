from copypaster.register import Register, register_instance
from copypaster.signal_bus import signal_bus
from copypaster import logger, CURRENT_DIR, State, NORMAL, AUTOSAVE, EDIT,  REMOVE

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio, GObject  # noqa

# translate = {
#     "Autosave": AUTOSAVE,
#     "Edit":     `EDIT, NORMAL, REMOVE
# }


class StateButtonsCallbacks:
    def on_autosave(self, button, name):
        self._deactive_rest_buttons('autosave')

        if button.get_active():
            self.state['app'] = AUTOSAVE
            signal_bus.emit('autosave_on')

            self.handle = self.clip.connect(
                'owner-change', self.auto_clipboard)
            logger.debug('Autosave on')
        else:
            signal_bus.emit('autosave_off')
            self.state['app'] = NORMAL
            self.clip.disconnect(self.handle)
            logger.debug('Autosave off')

    def on_edit(self, button, name):
        self._deactive_rest_buttons('edit')

        if button.get_active():
            self.state['app'] = EDIT
            logger.debug('Edit on')
        else:
            self.state['app'] = NORMAL
            logger.debug('Edit off')

    def on_add(self, button, name):
        logger.debug('Begin adding button')
        self._deactive_rest_buttons('edit')
        signal_bus.emit('add_button')
        # Register['NewNote'].add_new_button()

    def on_remove(self, button, name):
        self._deactive_rest_buttons('remove')

        if button.get_active():
            self.state['app'] = REMOVE
            logger.debug('Remove on')

        else:
            self.state['app'] = NORMAL
            logger.debug('Remove off')

    def auto_clipboard(self, clipboard, parameter):
        if self.state['app'] != AUTOSAVE:
            return False

        name = value = clipboard.wait_for_text()

        if not value:
            logger.error("No value to save - aborting")
            return False

        Register['NewNote'].add_button(name, value)

    def _deactive_rest_buttons(self, leave_alone):
        [button.set_active(False) for name, button in self.buttons.items(
        ) if name != leave_alone and button.get_active()]


@register_instance
class StateButtons(StateButtonsCallbacks, Gtk.Box):
    """Autosave, Edit, Remove"""

    def __init__(self, app_state):
        Gtk.Box.__init__(self, spacing=6)
        self.state = app_state

        self.buttons = {}

        self.clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.handle = None

        self._create_button("Autosave", self.on_autosave, "1")
        self._create_button("Edit", self.on_edit, "2")
        self._create_button("Remove", self.on_remove, "3")
        self._create_button("Add", self.on_add, "4")

    def _create_button(self, name, callback, ind):
        _button = Gtk.ToggleButton(name)
        _button.connect("toggled", callback, ind)

        self.pack_start(_button, True, True, 0)

        self.buttons[name.lower()] = _button

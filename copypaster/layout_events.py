from app.register import Register as __
from app.signal_bus import emit
from copypaster import log, State, AppState
from copypaster.file_loader import Copy, Snippet
from app.layout_events import LayoutEvents  # noqa

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa


class ToggleButtons:
    autosave = 'autosave'
    edit = 'edit'
    remove = 'remove'

    def names(self):
        return [ToggleButtons.autosave, ToggleButtons.edit, ToggleButtons.remove]

class Dialogs:
    def error_ok_pressed(self, button):
        log.debug("Close error dialog, on button click, emit close_error_dialog")
        emit("close_error_dialog")

    def save_folder(self, button):
        log.debug("Save folder, During click on Add button, emit save_folder")
        emit('save_folder')

    def save_snippet(self, *args, **kwargs):
        log.debug("Save snippet, During click on Add button, emit save_snippet")
        emit('save_snippet')

    def enter_save_snippet(self, widget, event):
        log.debug("Pressing enter when adding snippet")
        """
        Debuging functions:
        print("          Modifiers: ", event.state)
        print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))
        """

        # see if we recognise a keypress
        if event.keyval == Gdk.KEY_Return:
            emit('save_snippet')

    def enter_save_folder(self, widget, event):
        log.debug("During creating new folder, on enter")

        it_is_return = event.keyval == Gdk.KEY_Return
        if it_is_return:
            emit('save_folder')


class CopyPasterLayoutEvents(LayoutEvents, Dialogs):
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
        emit("add_button", Copy(Snippet(name, value)))

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
            emit("autosave_on")

            self.handle = self.clip.connect("owner-change", self.auto_clipboard)
            log.debug("Autosave on")
        else:
            emit("autosave_off")
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
        emit("open_add_button_dialog")

    def add_folder(self, button):
        log.debug("Begin adding folder")
        emit("open_add_folder_dialog")

Layout_events = CopyPasterLayoutEvents()

from app.register import Register as __
from app.signal_bus import subscribe
from app.signal_bus import emit
from copypaster import log, State, AppState
from copypaster.file_loader import Copy, Snippet

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa


class ToggleButtons:
    autosave = 'autosave'
    edit = 'edit'
    remove = 'remove'

    def names(self):
        return [ToggleButtons.autosave, ToggleButtons.edit, ToggleButtons.remove]


# dialogs

@subscribe
def enter_save_snippet(widget, event):
    log.debug("Pressing enter when adding snippet")
    """
    Debuging functions:
    print("          Modifiers: ", event.state)
    print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))
    """

    # see if we recognise a keypress
    if event.keyval == Gdk.KEY_Return:
        emit('save_snippet')

@subscribe
def enter_save_folder(widget, event):
    log.debug("During creating new folder, on enter")

    it_is_return = event.keyval == Gdk.KEY_Return
    if it_is_return:
        emit('save_folder')


# toolbar
def _deactive_rest_buttons(leave_alone):
    builder = __.Builder
    [
        builder.get_object(name).set_active(False)
        for name in ToggleButtons().names()
        if name != leave_alone and builder.get_object(name).get_active()
    ]

@subscribe
def autosave_on(button):
    _deactive_rest_buttons(ToggleButtons.autosave)

    if button.get_active():
        __.Jimmy.start_autosave()
    else:
        __.Jimmy.stop_autosave()

@subscribe
def edit_on(button):
    _deactive_rest_buttons(ToggleButtons.edit)

    if button.get_active():
        AppState["app"] = State.EDIT
        log.debug("Edit on")
    else:
        AppState["app"] = State.NORMAL
        log.debug("Edit off")

@subscribe
def remove_on(button):
    _deactive_rest_buttons(ToggleButtons.remove)

    if button.get_active():
        AppState["app"] = State.REMOVE
        log.debug("Remove on")

    else:
        AppState["app"] = State.NORMAL
        log.debug("Remove off")

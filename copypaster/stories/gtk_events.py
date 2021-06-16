from app.register import Register as __
from app.signal_bus import subscribe
from app.signal_bus import emit
from copypaster import log, State, AppState
from copypaster.file_loader import Copy, Snippet

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa





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

# rest of widgets

autosave = 'autosave'
edit = 'edit'
remove = 'remove'

names = [autosave, edit, remove]

def deactivate_all_except(activated_button):
    global names
    builder = __.Builder

    deactivate = lambda name: builder.get_object(name).set_active(False)
    is_active = lambda name: builder.get_object(name).get_active()

    [
        deactivate(button)
        for button in names
        if button is not activated_button and is_active(button)
    ]

@subscribe
def autosave_on(button):
    deactivate_all_except(autosave)

    if button.get_active():
        __.Jimmy.start_autosave()
    else:
        __.Jimmy.stop_autosave()

@subscribe
def edit_on(button):
    deactivate_all_except(edit)

    if button.get_active():
        __.AppState = __.State.EDIT

        log.debug("Edit on")
    else:
        __.AppState = __.State.NORMAL
        log.debug("Edit off")

@subscribe
def remove_on(button):
    deactivate_all_except(remove)

    if button.get_active():
        __.AppState = __.State.REMOVE
        log.debug("Remove on")

    else:
        __.AppState = __.State.NORMAL
        log.debug("Remove off")
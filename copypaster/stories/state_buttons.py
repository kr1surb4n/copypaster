from app.register import Register as __
from app.signal_bus import subscribe
from copypaster import log
import copypaster.events as event

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa


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
        __.State.edit
        log.debug("Edit on")
    else:
        __.State.normal
        log.debug("Edit off")


@subscribe
def remove_on(button):
    deactivate_all_except(remove)

    if button.get_active():
        __.State.remove
        log.debug("Remove on")

    else:
        __.State.normal
        log.debug("Remove off")

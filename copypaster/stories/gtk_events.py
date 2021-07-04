from app.register import Register as __
from app.signal_bus import subscribe
from app.signal_bus import emit
from copypaster import log
import copypaster.events as event

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa


# buttons on dialogs

@subscribe
def enter_saves_snippet(widget, gtk_event):
    log.debug("Pressing enter when adding snippet")
    """
    Debuging functions:
    print("          Modifiers: ", event.state)
    print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))
    """

    it_is_a_return = gtk_event.keyval == Gdk.KEY_Return
    if it_is_a_return:
        emit(event.save_snippet)


@subscribe
def enter_saves_folder(widget, gtk_event):
    log.debug("During creating new folder, on enter")

    it_is_a_return = gtk_event.keyval == Gdk.KEY_Return
    if it_is_a_return:
        emit(event.save_folder)
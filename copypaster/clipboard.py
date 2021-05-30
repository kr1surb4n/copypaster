import xerox
from app.register import register_instance
from app.register import Register as __
from app.signal_bus import emit
from copypaster import log, State, AppState

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa

# This is an abstraction for the actions
# done to clipboard.
#
# It's called Jimmy so that it's easier
# to talk about it.
# i.e.
# Jimmy failed to copy stuff.
# Jimmy cannot .
#


@register_instance
class Jimmy:
    """in tribute to Jimmy McGill, a copist"""

    def __init__(self):
        self.clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.handle = None

    def wait_for_data(self) -> str:
        return self.clip.wait_for_text()

    def start_autosave(self):
        self.handle = self.clip.connect("owner-change", self.auto_clipboard)
        log.debug("Autosave on")
        __.AppState = __.State.AUTOSAVE

    def stop_autosave(self):
        log.debug("Autosave off")    
        self.clip.disconnect(self.handle)
        self.handle = None
        __.AppState = __.State.NORMAL

    def send(self, text):
        log.debug("Coping: {}".format(text))
        xerox.copy(text)

    def clean_clipboard(self):
        log.debug("Cleaning clipboard")
        self.send("")

    def receive(self):
        contents = xerox.paste()
        log.debug("Pasting: {}".format(contents))
        return contents if contents.strip() else ""

    def auto_clipboard(self, clipboard, parameter):
        if __.AppState != __.State.AUTOSAVE:
            return False

        name = value = self.wait_for_data()
        if not value:
            log.error("No value to save - aborting")
            return False
        emit("add_button", name, value)

_Jimmy = Jimmy()


def test_jimmy():
    empty = ""

    # can I send and receive?
    test_message = "One, Two, Three"
    _Jimmy.send(test_message)
    assert _Jimmy.receive() == test_message

    # can I clean clipboard?
    _Jimmy.send(test_message)
    _Jimmy.clean_clipboard()
    assert _Jimmy.receive() != test_message
    assert _Jimmy.receive() == empty

from copypaster.state import AUTOSAVE
import copypaster.events as event
import xerox
from app.register import register_instance
from app.register import Register as __
from app.signal_bus import emit
from copypaster import log

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
        log.debug("Autosave on")
        self.handle = self.clip.connect("owner-change", self.auto_clipboard)
        __.State.autosave

    def stop_autosave(self):
        log.debug("Autosave off")
        self.clip.disconnect(self.handle)
        self.handle = None
        __.State.normal

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
        if not __.State.is_(AUTOSAVE):
            return False

        name = value = self.wait_for_data()
        if not value:
            log.error("No value to save - aborting")
            return False
        emit(event.add_button, name, value)


def test_jimmy():
    jimmy = Jimmy()

    test_message = "One, Two, Three"

    def can_i_send_and_receive(test_message):
        jimmy.send(test_message)
        assert jimmy.receive() == test_message

    can_i_send_and_receive(test_message)

    def can_i_clean_clipboard(test_message):
        empty = ""
        jimmy.send(test_message)
        jimmy.clean_clipboard()
        assert jimmy.receive() != test_message
        assert jimmy.receive() == empty

    can_i_clean_clipboard(test_message)

from app.register import Register as __
from app.signal_bus import emit
from folders import log, State, AppState
from app.layout_events import LayoutEvents  # noqa

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa


class FoldersLayoutEvents(LayoutEvents):
    def __init__(self):
        self.clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.handle = None


Layout_events = FoldersLayoutEvents()

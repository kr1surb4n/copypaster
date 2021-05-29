from app.register import Register as __
from app.signal_bus import emit
from copypaster import log, State, AppState
from copypaster.file_loader import Copy, Snippet
from app.layout_events import LayoutEvents  # noqa

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa


class CopyPasterLayoutEvents(LayoutEvents):
    def __getattr__(self, name):
        try:
            return super().__getattr__(self, name)
        except AttributeError:
            ...

        def method(*args, **kwargs):    
            emit(name, *args, **kwargs)
            
        return method

Layout_events = CopyPasterLayoutEvents()

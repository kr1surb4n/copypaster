from app.register import Register as __
from app.signal_bus import emit, signals
from app import log, State, AppState

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa


class LayoutEvents:
    def __getattr__(self, name):
        try:
            return super().__getattr__(self, name)
        except AttributeError:
            ...

        def method(*args, **kwargs):    
            emit(name, *args, **kwargs)
            
        return method

Layout_events = LayoutEvents()
__.Layout_events = Layout_events
from app.register import Register as __
from app.signal_bus import emit
from app import log, State, AppState

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa


class LayoutEvents:
    def __getattr__(self, name):
        """
        Code responsible for passing events from GTK
        to SignalBus.

        Get the method from the parent object
        if he implements that.

        If there is no such functions,
        create a function that will emit a signal/event
        with the name passed as argument, and return it.
       
        This way GTK triggering a callback is really
        triggering it in my Signal Bus.

        """
        try:
            return super().__getattr__(self, name)
        except AttributeError:
            ...

        def method(*args, **kwargs):    
            emit(name, *args, **kwargs)
            
        return method

Layout_events = LayoutEvents()
__.Layout_events = Layout_events


def test_LayoutEvents():
    raise NotImplementedError("LayoutEvents need tests")
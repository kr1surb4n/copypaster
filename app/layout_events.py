from app.register import register_instance
from app.signal_bus import emit
from app import log

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa

@register_instance
class LayoutEvents:
    def __getattr__(self, name):
        """
        Code responsible for passing events from GTK
        to SignalBus.

        Method:
        1. Get the method from the parent object
        if he implements that.

        2. If there is no such functions,
            a) create a function that will emit a signal/event
        with the name passed as argument, 
            b) and return it.


        This way GTK will be triggering a callback that
        will emit a signal to Signal Bus, with all the
        arguments. 

        """
        try:
            return super().__getattr__(self, name)
        except AttributeError:
            ...

        log.info(f"Routing event: {name}")
        def method(*args, **kwargs):
            emit(name, *args, **kwargs)

        return method


Layout_events = LayoutEvents()

def test_LayoutEvents():
    
    from app.signal_bus import signal_bus

    number_of_calls = 0

    def event():
        nonlocal number_of_calls
        number_of_calls += 1

    signal_bus.subscribe('event', event)


    assert number_of_calls == 0
    Layout_events.event()
    Layout_events.event()
    Layout_events.event()
    assert number_of_calls == 3

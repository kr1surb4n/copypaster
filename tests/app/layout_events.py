
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa

def test_LayoutEvents():
    from app.layout_events import LayoutEvents
    Layout_events = LayoutEvents()

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

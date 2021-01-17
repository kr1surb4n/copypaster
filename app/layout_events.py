from app.register import Register as __
from app.signal_bus import emit, signals
from app import log, State, AppState

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa


class LayoutEvents:
    def __init__(self):
        self.handle = None

    def about_button(self):
        pass

    def reload_css(self, *args):
        emit(signals.reload_default_styles)

    def on_quit_app(self, *args):
        __.Application.handle_quit('action', 'param')

    def quit_app(self, *args):
        self.on_quit_app(*args)


Layout_events = LayoutEvents()

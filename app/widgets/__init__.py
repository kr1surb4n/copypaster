from app.signal_bus import signal_bus, emit

from app.register import Register as __, register_instance

from app import log, CURRENT_DIR, State, AppState
import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio  # noqa


@register_instance
class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        log.debug("Lift off!")

        log.debug("App state NORMAL")
        AppState['app'] = State.NORMAL  # TODO: take out common from Register, signal_bus and make AppState out of it
        
        log.debug("Emitting start_app...")
        emit('start_app')

        log.debug("All green. Welcome to application.")

    def do_startup(self):
        log.debug("Startup...")

        Gtk.Application.do_startup(self)

        # important part when using GtkWindow with GtkBuilder
        self.add_window(__.main_window)
        __.main_window.show_all()

        log.debug('Menu loaded...')

    def handle_quit(self, action, parameter):
        log.debug("Emitting quit...")

        emit('quit')
        self.quit()

        log.debug("Goodbye! Application terminated.")


application = Application()
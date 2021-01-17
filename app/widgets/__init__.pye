from copypaster.signal_bus import signal_bus

from copypaster.register import Register as __, register_instance

from copypaster import log, CURRENT_DIR, State, AppState
import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio  # noqa


@register_instance
class MainWindow(Gtk.ApplicationWindow):

    screen = None
    calculated_width = 0
    calculated_height = 0

    def __init__(self, application):
        Gtk.ApplicationWindow.__init__(self, title="CopyPaster", application=application)
        log.debug("Calculating screen size...")
        self.screen = self.get_screen()

        self.calculate_size()

        self.set_default_size(self.calculated_width, self.calculated_height)

        self.set_resize_mode(Gtk.ResizeMode.PARENT)

    def calculate_size(self):
        self.calculated_width = int((self.screen.get_width() / 100) * 20)
        self.calculated_height = self.screen.get_height()

        __['calculated_width'] = self.calculated_width
        __['calculated_height'] = self.calculated_height


@register_instance
class Application(Gtk.Application):

    win = None

    def __init__(self):
        Gtk.Application.__init__(self)

        style_provider = Gtk.CssProvider()
        style_provider.load_from_path(os.path.join(CURRENT_DIR, "app.css"))

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def do_activate(self):
        log.debug("Lift off!")

        log.debug("App state NORMAL")
        AppState['app'] = State.NORMAL

        log.debug("Emitting start_app...")
        signal_bus.emit('start_app')

        log.debug("All green. Welcome to application.")

    def do_startup(self):
        log.debug("Startup...")

        Gtk.Application.do_startup(self)

        # important part when using GtkWindow with GtkBuilder
        self.add_window(__['MainWindow'])
        __['MainWindow'].show_all()

        log.debug('Menu loaded...')

    def handle_quit(self, action, parameter):
        log.debug("Emitting quit...")

        signal_bus.emit('quit')
        self.quit()

        log.debug("Goodbye! Application terminated.")

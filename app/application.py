from app import log
from app.signal_bus import event
from app.register import Register as __, register_instance


import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa


@register_instance
class Application(Gtk.Application):
    def __init__(self):
        super(Gtk.Application, self).__init__()

    def do_activate(self):
        log.info("Activation...")
        __.SignalBus.emit(event.activate_app)

    def do_startup(self):
        log.info("Startup...")
        __.SignalBus.emit(event.start_app)
        Gtk.Application.do_startup(self)

        # important part when using GtkWindow with GtkBuilder
        self.add_window(__.MainWindow)
        __.MainWindow.show_all()

    def handle_quit(self, action, parameter):
        log.info("Quiting...")
        self.quit()
        log.info("Goodbye! Application terminated.")

from app import log
from app.signal_bus import emit, event
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
        emit(event.activate_app)

    def do_startup(self):
        log.info("Startup...")
        emit(event.start_app)
        Gtk.Application.do_startup(self)

        # important part when using GtkWindow with GtkBuilder
        self.add_window(__.MainWindow)
        __.MainWindow.show_all()

    def handle_quit(self, action, parameter):
        log.info("Quiting...")
        self.quit()
        log.info("Goodbye! Application terminated.")


application = Application()


def test_application_object():
    # prepare the event handlers
    application = Application()
    from app.signal_bus import signal_bus

    activated = False
    started = False

    def activate_app():
        nonlocal activated
        activated = True

    def start_app():
        nonlocal started
        started = True

    signal_bus.subscribe(event.activate_app, activate_app)
    signal_bus.subscribe(event.start_app, start_app)

    assert isinstance(application, Gtk.Application)

    # run and test if handlers where run
    from time import sleep
    import threading

    def run():
        application.run()

    tested_thread = threading.Thread(target=run)
    tested_thread.start()
    sleep(1)
    assert started and activated

    del application
    del tested_thread

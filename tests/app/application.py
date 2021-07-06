from app import log
from app.signal_bus import emit, event
from app.register import Register as __, register_instance


import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa


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

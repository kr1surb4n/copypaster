# -*- coding: utf-8 -*-
import sys
import os

from app import log, CURRENT_DIR, AppState, State
from app.register import Register as __


def main_function(config_file):
    # create and run the application,
    # exit with the value returned by
    # running the program
    log.debug("Initializing services...")

    from app.config import config  # noqa

    config.load_config_file(config_file)
    __.AppState = AppState
    __.State = State
    __.AppState = __.State.INIT

    from app.widgets import application  # noqa
    import app.style  # noqa

    log.debug("Loading Widgets usig GtkBuilder...")
    from app.builder import builder  # noqa
    from app.layout_events import Layout_events

    builder.set_application(application)  # works without it
    builder.add_from_file(os.path.join(CURRENT_DIR, "layout.glade"))
    builder.connect_signals(Layout_events)

    __.main_window = builder.get_object("main_window")
    __.welcome_sign = builder.get_object("welcome_sign")

    log.debug("Importing stories...")
    import app.stories  # noqa

    log.debug("Starting1 the Application...")
    exit_status = application.run()

    log.debug("Returning exit status value...")
    return exit_status


def test_main_function():
    from time import sleep
    import threading

    tested_thread = threading.Thread(target=main_function, args=("test_config",))
    tested_thread.start()

    sleep(2)
    print(dir(tested_thread))
    global __

    assert tested_thread.is_alive()
    assert __.Config
    assert __.SignalBus
    assert __.Application
    assert __.Builder
    assert __.main_window
    assert __.welcome_sign
    assert __.welcome_sign.get_text() == "I am Kr15 GTK App"

    __.Application.handle_quit('action', 'param')
    # assert __.Application is not None
    # assert __.Config is not None

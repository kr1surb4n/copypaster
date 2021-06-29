# -*- coding: utf-8 -*-
import os

from app import log, CURRENT_DIR
from app.register import Register as __


def main_function(config_file):
    # create and run the application,
    # exit with the value returned by
    # running the program
    log.info("Initializing services...")

    from app.config import config  # noqa
    config.load_config_file(config_file)


    from app.state import State, INIT, NORMAL
    state = State([INIT, NORMAL])

    from app.application import application  # noqa
    import app.style # noqa

    log.info("Loading Widgets usig GtkBuilder...")
    from app.builder import builder  # noqa
    from app.layout_events import Layout_events

    builder.set_application(application)  # works without it
    builder.add_from_file(os.path.join(CURRENT_DIR, "layout.glade"))
    builder.connect_signals(Layout_events)

    __.MainWindow = builder.get_object("main_window")
    __.WelcomeSign = builder.get_object("welcome_sign")

    log.info("Importing stories...")
    import app.stories  # noqa
    
    log.info("Starting the Application...")
    exit_status = application.run()

    log.info("Returning exit status value...")
    return exit_status


def test_main_function():
    from time import sleep
    import threading

    tested_thread = threading.Thread(target=main_function, args=("test_config",))
    tested_thread.start()

    sleep(2)
    global __

    assert tested_thread.is_alive()
    assert __.State
    assert __.Config
    assert __.SignalBus
    assert __.Application
    assert __.Builder
    assert __.LayoutEvents
    assert __.MainWindow
    assert __.WelcomeSign
    assert __.WelcomeSign.get_text() == "I am Kr15 GTK App"

    __.Application.handle_quit('action', 'param')
    tested_thread.join()
    assert not tested_thread.is_alive()
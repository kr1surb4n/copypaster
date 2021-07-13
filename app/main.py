# -*- coding: utf-8 -*-
from app.application import Application
import os

from app import log, CURRENT_DIR

def main_function(config_file):
    # create and run the application,
    # exit with the value returned by
    # running the program
    log.info("Initializing services...")

    from app.register import Register as __
    from app.config import Config  # noqa
    from app.application import Application  # noqa
    from app.style import Style  # noqa
    from app.state import State, INIT, NORMAL
    from app.builder import Builder  # noqa
    from app.layout_events import LayoutEvents

    application = Application()
    config = Config()
    config.load_config_file(config_file)
    state = State([INIT, NORMAL])

    style = Style()
    __.Style.registry.append(os.path.join(CURRENT_DIR, "styles/app.css"))

    log.info("Loading Widgets usig GtkBuilder...")
    builder = Builder()
    layout_events = LayoutEvents()

    builder.set_application(application)  # works without it
    builder.add_from_file(os.path.join(CURRENT_DIR, "layout.glade"))
    builder.connect_signals(layout_events)

    __.MainWindow = builder.get_object("main_window")
    __.WelcomeSign = builder.get_object("welcome_sign")

    log.info("Importing stories...")
    import app.stories  # noqa

    log.info("Starting the Application...")
    exit_status = application.run()

    log.info("Returning exit status value...")
    return exit_status

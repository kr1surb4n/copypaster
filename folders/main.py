# -*- coding: utf-8 -*-
import sys
import os
import configparser

from folders import log, PROJECT_DIR, dupa
from app.signal_bus import emit
from app.register import register_instance, Register as __

""" Initialize services """

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa

GLADE_FILE = os.path.join(PROJECT_DIR, "folders/layout.glade")

WORKBENCH = 'Workbench'
MAIN_WINDOW = "main_window"
MAIN_BOX = "main_box"
WORKBENCH_LOCATION = "workbench_location"


def main_function(config_file):
    # create and run the application, exit with the value returned by
    # running the program

    log.info("Initializing services...")
    import app.style  # noqa
    from app.widgets import application  # noqa

    from folders.builder import builder  # noqa

    import app.config  # noqa

    # TODO: still loding config file from the repository
    # config_file = os.path.join(PROJECT_DIR, "config/example.conf")
    # __.Config.load_config_file(config_file)

    log.debug("Loading Widgets usig GtkBuilder...")
    builder.set_application(application)  # works without it
    builder.add_from_file(GLADE_FILE)

    __.main_window = builder.get_object(MAIN_WINDOW)
    __.main_box = builder.get_object(MAIN_BOX)
    __.workbench = builder.get_object(WORKBENCH.lower())
    __.workbench_location = builder.get_object(WORKBENCH_LOCATION)

    # load the events
    from folders.layout_events import Layout_events  # noqa

    builder.connect_signals(Layout_events)

    log.debug("Importing stories...")
    import folders.stories  # noqa

    emit('load_style', os.path.join(PROJECT_DIR, "folders", "app.css"))

    log.debug("Starting the Application...")
    exit_status = application.run(sys.argv)

    log.debug("Returning exit status value...")
    return exit_status

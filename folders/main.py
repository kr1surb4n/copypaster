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


def main_function(config_file):
    # create and run the application, exit with the value returned by
    # running the program

    log.debug("Initializing services...")
    import app.style  # noqa
    from app.widgets import application  # noqa

    from app.builder import builder  # noqa

    import app.config  # noqa

    # TODO: still loding config file from the repository
    # config_file = os.path.join(PROJECT_DIR, "config/example.conf")
    # __.Config.load_config_file(config_file)

    log.debug("Loading Widgets usig GtkBuilder...")
    builder.set_application(application)  # works without it
    builder.add_from_file("app/layout.glade")

    __.main_window = builder.get_object("main_window")
    __.main_box = builder.get_object("main_box")

    welcome_sing = builder.get_object("welcome_sign")
    __.main_box.remove(welcome_sing)

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

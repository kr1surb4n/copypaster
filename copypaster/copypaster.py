# -*- coding: utf-8 -*-
import sys
import os

from copypaster import log, PROJECT_DIR  #, dupa
from app.register import Register as __

""" Initialize services """

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa


def main_function(config_file):
    """ create and run the application, 
    exit with the value returned by
    running the program"""

    log.debug("Initializing services...")

    import app.style  # noqa
    import copypaster.clipboard  # noqa

    from app.widgets import application  # noqa
    from copypaster.builder import builder  # noqa
    from app.config import config  # noqa

    config.load_config_file(config_file)

    log.debug("Loading Widgets usig GtkBuilder...")

    __.Builder.set_application(application)  # works without it
    __.Builder.add_from_file("copypaster/layout.glade")

    __.main_window = builder.get_object("main_window")
    __.Snippets = builder.get_object("snippets")
    __.StateButtons = builder.get_object("toolbar")


    from copypaster.layout_events import Layout_events  # noqa
    __.Builder.connect_signals(Layout_events)

    log.debug("Importing stories...")
    import copypaster.stories  # noqa

    log.debug("Starting the Application...")
    exit_status = application.run(sys.argv)

    log.debug("Returning exit status value...")
    return exit_status

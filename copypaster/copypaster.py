# -*- coding: utf-8 -*-
from app import builder, layout_events
import os
from copypaster import log, CURRENT_DIR  # noqa
from app.register import Register as __

""" Initialize services """

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa


def main_function(config_file=None):
    """create and run the application,
    exit with the value returned by
    running the program"""

    log.info("Initializing services...")
  
    from app.style import Style # noqa
    from app.application import Application  # noqa
    from app.builder import Builder  # noqa
    from app.layout_events import LayoutEvents  # noqa
    from app.config import Config  # noqa
    from app.state import State
    from copypaster.clipboard import Jimmy # noqa
    from copypaster.state import INIT, NORMAL, AUTOSAVE, EDIT, REMOVE
    import app.stories  # noqa
    
    style = Style()
    application =  Application()
    builder = Builder()
    layout_events = LayoutEvents()
    jimmy = Jimmy()
    state = State([INIT, NORMAL, EDIT, REMOVE, AUTOSAVE])
    config = Config()
    config.load_config_file(config_file)

    __.Style.registry.append(os.path.join(CURRENT_DIR, "app.css"))

    log.info("Loading Widgets usig GtkBuilder...")

    from copypaster.widgets.containers import ButtonTree

    __.Builder.add_custom_object('ButtonTree', ButtonTree)

    __.Builder.set_application(application)  # works without it

    __.Builder.add_from_file("copypaster/layout.glade")
    __.Builder.add_from_file("copypaster/dialogs.glade")

    __.MainWindow = builder.get_object("main_window")

    __.error_dialog = builder.get_object("error_dialog")
    __.folder_dialog = builder.get_object("folder_dialog")
    __.snippet_dialog = builder.get_object("snippet_dialog")

    __.Snippets = builder.get_object("snippets")
    __.StateButtons = builder.get_object("toolbar")
    __.PreviewLabel = builder.get_object("preview_label")
    __.LevelIndicator = builder.get_object("current_level")

    __.Builder.connect_signals(layout_events)

    log.info("Importing stories...")
    import copypaster.stories  # noqa

    log.info("Starting the Application...")
    # exit_status = application.run(sys.argv)
    exit_status = application.run()

    log.info("Returning exit status value...")
    return exit_status

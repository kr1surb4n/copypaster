# -*- coding: utf-8 -*-
import sys
import os

from copypaster import log, PROJECT_DIR, dupa, AppState, State  # noqa
from app.register import Register as __

""" Initialize services """

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa


def main_function(config_file=None):
    """create and run the application,
    exit with the value returned by
    running the program"""

    log.debug("Initializing services...")

    import app.style  # noqa
    import app.stories  # noqa
    from app.widgets import application  # noqa
    from app.builder import builder  # noqa
    from app.config import config  # noqa

    import copypaster.clipboard  # noqa

    config.load_config_file(config_file)

    __.AppState = AppState
    __.State = State
    __.AppState = State.INIT

    log.debug("Loading Widgets usig GtkBuilder...")

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

    from app.layout_events import Layout_events  # noqa

    __.Builder.connect_signals(Layout_events)

    log.debug("Importing stories...")
    import copypaster.stories  # noqa

    log.debug("Starting the Application...")
    # exit_status = application.run(sys.argv)
    exit_status = application.run()

    log.debug("Returning exit status value...")
    return exit_status

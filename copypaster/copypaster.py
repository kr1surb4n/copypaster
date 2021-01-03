# -*- coding: utf-8 -*-
import sys
import os
import configparser

from copypaster import log
from copypaster.register import register_instance, Register
from copypaster.widgets import Application, MainWindow
from copypaster.widgets.notebooks import FileCabinet

""" Initialize services """

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa


class GtkBuilder(Gtk.Builder):
    def do_get_type_from_name(self, type_name):
        """
        Looks up a type by name, using the virtual function that Gtk.Builder
        has for that purpose.

        Parameters:  type_name (str) – type name to lookup
        Returns:     the GObject.GType found for type_name
                       or GObject.TYPE_INVALID if no type was found
        Return type: GObject.GType

        """

        if type_name == 'MainWindow':
            return MainWindow

        if type_name == 'FileCabinet':
            return FileCabinet

        if type_name == 'Application':
            return Application

        r = Gtk.Builder.do_get_type_from_name(self, type_name)
        print('GtkBuilder: => {}\t{}'.format(type_name, r))
        return r


@register_instance
class Config:
    cfg = None

    def __init__(self, config_file=None):
        log.debug("Initializing config...")
        config_env = os.environ.get("COPYPASTER_CONFIG", None)

        if config_env is not None:
            config = config_env
        elif config_file is not None:
            config = config_file

        self.cfg = configparser.ConfigParser()
        self.cfg.read(config)

    def get_dirty_deck(self):
        try:
            main = self.cfg["main"]
            return "Dirty", main["dirty_deck"]
        except IndexError as _e:
            print(_e)
            raise _e

    def get_decks(self):
        try:
            filepaths = self.cfg["decks"]
            return {deck_name: filepaths[deck_name] for deck_name in filepaths}
        except IndexError as _e:  # watch out! snakes
            print(_e)
            raise _e

    def get_collections(self):
        try:
            filepaths = self.cfg["collections"]
            return {
                collection_name: filepaths[collection_name]
                for collection_name in filepaths
            }
        except IndexError as _e:  # well, it's python. what did you exepect?
            print(_e)
            raise _e


def main_function(config):
    # create and run the application, exit with the value returned by
    # running the program

    Config(config)

    # TODO:
    # - DONE change the theme in visual studio
    #   C+, - in settings.json reloads theme
    # - open glade and see the objects

    # theater:
    #     menu:
    #       want_new_notebook
    #       want_open_notebook
    #       want_save_notebook
    #       want_saveas_notebook

    #       quit: on_quit_app

    #     toolbar:
    #       autosave: autosave_on
    #       edit: edit_on
    #       remove: remove_on
    #       add: add
    #       remove_notebook: remove_notebook
    #     file_cabinet:
    # - go through the widgets and see where are imports
    # StateButtons go away. You need to move the callbacks to other
    # handle, and connect to toolbox object from glade.
    # - go through the stories and see where the widgets are used

    app = Application()

    log.debug("Loading Widgets usig GtkBuilder...")
    builder = GtkBuilder()
    builder.set_application(app)  # works without it
    builder.add_from_file("copypaster/layout.glade")

    Register['Builder'] = builder
    Register['MainWindow'] = builder.get_object("main_window")
    Register['FileCabinet'] = builder.get_object("file_cabinet")
    Register['StateButtons'] = builder.get_object("toolbar")

    from copypaster.layout_events import Layout_events

    builder.connect_signals(Layout_events)

    log.debug("Initializing services...")
    import copypaster.clipboard  # noqa

    log.debug("Importing stories...")
    import copypaster.stories  # noqa

    log.debug("Starting the Application...")
    exit_status = app.run(sys.argv)

    log.debug("Returning exit status value...")
    return exit_status

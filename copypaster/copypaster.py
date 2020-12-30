# -*- coding: utf-8 -*-
import sys
import os
import configparser

from copypaster import log
from copypaster.register import register_instance
from copypaster.widgets import Application

""" Initialize services """


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

    #     toolbar:
    #       autosave: autosave_on
    #       edit: edit_on
    #       remove: remove_on
    #       add: add

    #     file_cabinet:
    # - go through the widgets and see where are imports

    # - go through the stories and see where the widgets are used

    # What does application do?
    # When add the builder code?
    app = Application()

    log.debug("Importing stories...")
    import copypaster.stories  # noqa

    exit_status = app.run(sys.argv)
    log.debug("Returning exit status value...")
    return exit_status

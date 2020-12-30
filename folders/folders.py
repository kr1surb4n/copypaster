# -*- coding: utf-8 -*-
import sys
import os
import configparser

from folders import log
from folders.register import register_instance
from folders.widgets import Application

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

    app = Application()

    log.debug("Importing stories...")
    import folders.stories  # noqa

    exit_status = app.run(sys.argv)
    log.debug("Returning exit status value...")
    return exit_status

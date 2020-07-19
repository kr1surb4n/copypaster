# -*- coding: utf-8 -*-
import sys
import os
import configparser

from copypaster import PROJECT_DIR, State, logger
from copypaster.register import Register, register_instance
from copypaster.widgets import Application

""" Initialize services """
import copypaster.clipboard


@register_instance
class Config:
    cfg = None

    def __init__(self, config_file=None):
        logger.debug("Initializing config...")
        config_env = os.environ.get('COPYPASTER_CONFIG', None)

        if config_env is not None:
            config = config_env
        elif config_file is not None:
            config = config_file

        self.cfg = configparser.ConfigParser()
        self.cfg.read(config)

    def get_dirty_deck(self):
        try:
            main = self.cfg['main']
            return 'Dirty', main['dirty_deck']
        except IndexError as e:
            print(e)
            raise e

    def get_decks(self):
        try:
            decks = self.cfg['decks']
            return {sec: decks[sec] for sec in decks}
        except IndexError as e:
            print(e)
            raise e

    def get_collections(self):
        try:
            collections = self.cfg['collections']
            return {sec: collections[sec] for sec in collections}
        except IndexError as e:
            print(e)
            raise e


def main_function(config):
    # create and run the application, exit with the value returned by
    # running the program

    Config(config)

    app = Application()

    logger.debug("Importing stories...")
    import copypaster.stories

    exit_status = app.run(sys.argv)
    logger.debug("Returning exit status value...")
    return exit_status

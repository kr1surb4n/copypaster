# -*- coding: utf-8 -*-
import sys
import os
import configparser

from copypaster import PROJECT_DIR
from copypaster.register import Register, register_instance
from copypaster.widgets import Application

""" Initialize services """
import copypaster.clipboard
#import copypaster.file_loader


@register_instance
class Config:
    cfg = None

    def __init__(self, config_file=None):
        config_env = os.environ.get('COPYPASTER_CONFIG', None)

        if config_env is not None:
            config = config_env
        elif config_file is not None:
            config = config_file

        self.cfg = configparser.ConfigParser()
        self.cfg.read(config)

    def get_dirty_deck(self):
        try:
            return 'Dirty', self.cfg['main']['dirty_deck']
        except IndexError as e:
            print(e)
            raise e

    def get_decks(self):
        try:
            return {sec: self.cfg['decks'][sec] for sec in self.cfg['decks']}
        except IndexError as e:
            print(e)
            raise e


def main_function():
    # create and run the application, exit with the value returned by
    # running the program
    app = Application()
    exit_status = app.run(sys.argv)
    return exit_status

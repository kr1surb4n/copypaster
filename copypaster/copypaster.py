# -*- coding: utf-8 -*-
import sys
import os
import configparser

from copypaster import PROJECT_DIR
from copypaster.register import Register, register_instance
from copypaster.widgets import Application

""" Initialize services """
from copypaster.clipboard import Jimmy
from copypaster.file_loader import Deck

"""Main module."""


@register_instance
class Config:
    cfg = None

    def __init__(self, config_file=None):
        config_env = os.environ('COPYPASTER_CONFIG', None)

        if config_env is not None:
            config = config_env
        elif config_file is not None:
            config = config_file
        else:
            config = os.path.join(PROJECT_DIR, "config/example.conf")

        self.cfg = configparser.ConfigParser()
        self.cfg.read(config)


def main_function():
    # create and run the application, exit with the value returned by
    # running the program
    app = Application()
    exit_status = app.run(sys.argv)
    return exit_status

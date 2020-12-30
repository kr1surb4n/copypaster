# -*- coding: utf-8 -*-

"""Top-level package for Copypaster."""

# Hello!
__author__ = """Przemek Kot"""
__email__ = "kris@whereibend.space"
__version__ = "0.1.0"

import logging
import os

# usefull paths
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

# initialize logger
# TODO change name to 'log'
log = logging.getLogger("CopyPaster")
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

log.addHandler(ch)


class State(dict):
    NORMAL = "NORMAL"
    AUTOSAVE = "AUTOSAVE"
    REMOVE = "REMOVE"
    EDIT = "EDIT"


# SET INITIAL STATE
AppState = {"app": State.NORMAL}  # global application state

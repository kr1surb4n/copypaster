# -*- coding: utf-8 -*-

"""Top-level package for Copypaster."""

# Hello!
__author__ = """Przemek Kot"""
__email__ = "kris@plumplum.space"
__version__ = "0.1.0"
from functools import wraps
import logging
import os

# usefull paths
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

# initialize logger
log = logging.getLogger("CopyPaster")
log.setLevel(logging.DEBUG)
logging.info("Start Copypaster")


class State(dict):
    NORMAL = "NORMAL"
    AUTOSAVE = "AUTOSAVE"
    REMOVE = "REMOVE"
    EDIT = "EDIT"


# SET INITIAL STATE
AppState = {"app": State.NORMAL}  # global application state


dupa_counter = 1


def dupa():
    global dupa_counter
    print(f"DUPA {dupa_counter}")
    dupa_counter += 1


def decorate_with_dupa(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        dupa()
        return func(*args, **kwargs)

    return wrapper

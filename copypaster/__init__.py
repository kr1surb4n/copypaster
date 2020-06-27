# -*- coding: utf-8 -*-

"""Top-level package for Python Boilerplate."""

__author__ = """Kris Urbanski"""
__email__ = 'kris@whereibend.space'
__version__ = '0.1.0'

import logging
import os

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

logger = logging.getLogger('CopyPaster')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)


class State(dict):
    NORMAL = 'NORMAL'
    AUTOSAVE = 'AUTOSAVE'
    REMOVE = 'REMOVE'
    EDIT = 'EDIT'


# SET INITIAL STATE
AppState = {'app': State.NORMAL}  # global application state

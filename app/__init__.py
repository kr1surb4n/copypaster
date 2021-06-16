# -*- coding: utf-8 -*-

"""Top-level package for Copypaster."""

# Hello!
__author__ = """Kris Urbanski"""
__email__ = "kris@plumplum.space"
__version__ = "0.1.0"

import logging
import os

# usefull paths
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

# initialize logger
log = logging.getLogger("Kr15 App")
log.setLevel(logging.WARN)


class State:
    INIT = "INIT"
    NORMAL = "NORMAL"


# SET INITIAL STATE
AppState = State.NORMAL  # global application state

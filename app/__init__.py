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
log.setLevel(logging.INFO)


class sss:
    def info(self, t):
        print(t)

    def critical(self, t):
        print(t)

    def setLevel(self, x):
        ...

log = sss()
#log.setLevel(logging.WARN)
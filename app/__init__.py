# -*- coding: utf-8 -*-

"""Top-level package for Kr15 Mini GTK App Framework."""

# Hello!
__author__ = """Kris Urbanski"""
__email__ = "kris@plumplum.space"
__version__ = "0.1.0"

import logging
import os
import sys

# usefull paths
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

# initialize logger
logging.basicConfig(
    level=logging.WARN,
    format='[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
)
log = logging.getLogger("Kr15 App")


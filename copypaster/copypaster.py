# -*- coding: utf-8 -*-
import sys
from copypaster.widgets import Application

"""Main module."""
def main_function():
    # create and run the application, exit with the value returned by
    # running the program
    app = Application()
    exit_status = app.run(sys.argv)
    return exit_status

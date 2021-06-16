# -*- coding: utf-8 -*-

"""Console script for app."""
import sys
import click
from app import log, PROJECT_DIR
from app.main import main_function
import logging

from os.path import expanduser

default_config_path = expanduser("~/.config/app.conf")


@click.command()
@click.option("--config", default=default_config_path)
@click.option('--debug', is_flag=True, default=False, help='turn log level DEBUG on')
def main(config, debug):
    """Console script for app."""
    if debug:
        log.setLevel(logging.DEBUG)

    log.info("Started Kr15 Gtk App")

    try:
        pass
        main_function(config)
    except Exception as e:
        log.critical(str(e))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

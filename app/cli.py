# -*- coding: utf-8 -*-

"""Console script for app."""
import sys
import click
from app import log
from app.main import main_function

from os.path import expanduser

default_config_path = expanduser("~/.config/app.conf")


@click.command()
@click.option("--config", default=default_config_path)
@click.option('--debug', is_flag=True, default=False, help='turn log level DEBUG on')
@click.option('--profile', is_flag=True, default=False, help='turn profiling on')
def main(config, debug, profile):
    """Console script for app."""
    if debug:
        import logging
        log.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)


    log.info("Started Kr15 Gtk App")

    try:
        main_function(config)
    except Exception as e:
        log.critical(str(e))
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

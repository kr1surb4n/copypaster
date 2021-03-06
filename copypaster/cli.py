# -*- coding: utf-8 -*-

"""Console script for copypaster."""
import sys
import click
from os.path import expanduser
import logging

from app import log as applog
from copypaster import log
from copypaster.copypaster import main_function


default_config_path = expanduser("~/.config/copypaster.conf")


@click.command()
@click.option("--config", default=default_config_path)
@click.option('--debug', is_flag=True, default=False, help='turn log level DEBUG on')
def main(config, debug):
    """Console script for copypaster."""

    if debug:
        applog.setLevel(logging.DEBUG)
        log.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)

    log.info("Started CopyPaster")
    log.info("copypaster.cli.main")

    try:
        main_function(config)
    except Exception as e:
        log.critical(str(e))
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

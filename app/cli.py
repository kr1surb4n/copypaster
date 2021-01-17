# -*- coding: utf-8 -*-

"""Console script for app."""
import os
import sys
import click
from app import log, PROJECT_DIR
from app.main import main_function

from os.path import expanduser

default_config_path = expanduser("~/.config/app.conf")


@click.command()
@click.option("--config", default=default_config_path)
def main(config):
    """Console script for app."""
    log.info("Started Kr15 Gtk App")
    log.info("app.cli.main")

    try:
        pass
        main_function(config)
    except Exception as e:
        log.critical(str(e))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

# -*- coding: utf-8 -*-

"""Console script for copypaster."""
import os
import sys
import click
from copypaster import logger, PROJECT_DIR
from copypaster.copypaster import main_function, Config

default_config = os.path.join(PROJECT_DIR, "config/example.conf")


@click.command()
@click.option('--config', default=default_config)
def main(config):
    """Console script for copypaster."""
    logger.info("Started program")

    return main_function(config)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

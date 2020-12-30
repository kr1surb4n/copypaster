# -*- coding: utf-8 -*-

"""Console script for copypaster."""
import os
import sys
import click
from copypaster import log, PROJECT_DIR
from copypaster.copypaster import main_function

default_config_path = os.path.join(PROJECT_DIR, "config/example.conf")


@click.command()
@click.option("--config", default=default_config_path)
def main(config):
    """Console script for copypaster."""
    log.info("Started CopyPaster")
    log.info("copypaster.cli.main")

    return main_function(config)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

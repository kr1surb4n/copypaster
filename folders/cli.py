# -*- coding: utf-8 -*-

"""Console script for folders."""
import os
import sys
import click
from folders import log, PROJECT_DIR
from folders.folders import main_function

default_config_path = os.path.join(PROJECT_DIR, "config/example.conf")


@click.command()
@click.option("--config", default=default_config_path)
def main(config):
    """Console script for folders."""
    log.info("Started CopyPaster")

    return main_function(config)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

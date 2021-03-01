# -*- coding: utf-8 -*-

"""Console script for copypaster."""
import sys
import click
from copypaster import log


from copypaster.copypaster import main_function

from os.path import expanduser

default_config_path = expanduser("~/.config/copypaster.conf")


@click.command()
@click.option("--config", default=default_config_path)
def main(config):
    """Console script for copypaster."""
    log.info("Started CopyPaster")
    log.info("copypaster.cli.main")

    try:
        pass
        main_function(config)
    except Exception as e:
        log.critical(str(e))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

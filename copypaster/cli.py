# -*- coding: utf-8 -*-

"""Console script for copypaster."""
import sys
import click

from copypaster.copypaster import main_function

@click.command()
def main(args=None):
    """Console script for copypaster."""
    click.echo("Replace this message by putting your code into "
               "copypaster.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")

    return main_function()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

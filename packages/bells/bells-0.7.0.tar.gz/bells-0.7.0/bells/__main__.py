"Main script for bells"
import logging
import sys

import click
from .commands import init, rec, rec_file
from . import __version__


@click.group(invoke_without_command=True)
@click.option("-v", "--verbose", is_flag=True,
              help="Verbose mode for printing debug info")
@click.option("--version", is_flag=True,
              help="Print version")
@click.pass_context
def main(ctx, verbose, version):
    "Bells is a project for storing voice recordings"
    level = logging.WARN
    if verbose:
        level = logging.DEBUG
    logging.basicConfig(level=level)
    if version:
        print(__version__)
        return

    if ctx.invoked_subcommand is None:
        if len(sys.argv) > 1:
            ctx.fail("Missing command.")
        print(ctx.get_help())


main.add_command(init)
main.add_command(rec)
main.add_command(rec_file)

if __name__ == '__main__':
    main()  # pylint: disable=E1120

"""show current link of the `.env` file."""
import os

import click

from chenv import settings
from chenv.cli import cli
from chenv.console import as_link, Color


@cli.command(help="show current link of the `.env` file.")
def which() -> None:
    """Show current link of the `.env` file."""
    try:
        target = os.readlink(settings.DOTENV)
        if os.path.exists(target):
            click.echo(as_link(target, Color.BRIGHT_GREEN))
        else:
            click.echo(f"{as_link(target, Color.RED)}" " (broken, links to non-existent file).")
    except FileNotFoundError:
        click.echo(f'{as_link("null", Color.YELLOW)} (does not link to any file).')

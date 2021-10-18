"""Command-line interface."""
from typing import Optional

import click
from click.core import Context

from chenv import fs, settings, transform
from chenv.console import as_link, Color, fatal
from chenv.models.output import Output
from . import __version__

settings.mount()


@click.group()
@click.pass_context
@click.version_option(version=__version__)
def cli(ctx: Context) -> None:
    """chenv. modern local environment management."""
    click.secho("chenv. modern local environment management", fg=Color.GREEN.value)


@cli.resultcallback()
def _pipeline(result: Optional[Output]) -> None:
    try:
        if result is None or result.file_suffix is None:
            return

        transformed_output: Output = transform.apply(result)
        fs.assign_env(transformed_output.filename, transformed_output.variables)
        click.echo(as_link(result.filename, Color.BRIGHT_GREEN))
    except Exception as e:
        fatal(__name__, f"{e.__class__.__name__} - {str(e)}", 1)

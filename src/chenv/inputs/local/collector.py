"""choose between local, existing, .env files."""
import os
from typing import Optional

import click
import questionary

from chenv import settings
from chenv.cli import cli
from chenv.console import fatal
from chenv.models.output import Target


@cli.command("local", help="choose between local, existing, .env files")
@click.argument("filename", required=False, metavar="filename")
def collect(filename: Optional[str]) -> Target:
    """Choose between local, existing, .env files."""
    if filename:
        filename = filename.replace(settings.PREFIX, "")
        if os.path.exists(settings.filename_from_template(filename)):
            return Target(file_suffix=filename)

    env_files = sorted(
        filename.replace(settings.PREFIX, "")
        for filename in os.listdir(".")
        if filename.startswith(settings.PREFIX)
    )

    if not env_files:
        fatal(__name__, "No local options available.", 2)

    click.echo(
        f"""Local options: {", ".join(click.style(env_file, fg="magenta")
         for env_file in env_files)}"""
    )
    env_file = questionary.autocomplete("Choose file:", choices=env_files).ask()
    return Target(file_suffix=env_file)

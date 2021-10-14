"""choose between local, existing, .env files."""
import os
from typing import Optional

import click
import questionary

from chenv import fs, settings
from chenv.cli import cli
from chenv.console import fatal, pretty_failures
from chenv.models.output import Output


@cli.command("local", help="choose between local, existing, .env files")
@click.argument("filename", required=False, metavar="filename")
@pretty_failures
def collect(filename: Optional[str]) -> Output:
    """Choose between local, existing, .env files."""
    file_suffix = (filename or "").replace(settings.PREFIX, "")
    if file_suffix:
        if not os.path.exists(fs.filename_from_template(file_suffix)):
            fatal(__name__, f"No file found for `{filename}`", 2)

    else:
        env_files = sorted(
            file_option.replace(settings.PREFIX, "")
            for file_option in os.listdir(".")
            if file_option.startswith(settings.PREFIX)
        )

        if not env_files:
            fatal(__name__, "No local options available.", 2)

        click.echo(
            f"""Local options: {", ".join(click.style(env_file, fg="magenta")
            for env_file in env_files)}"""
        )
        file_suffix = questionary.autocomplete("Choose file:", choices=env_files).ask()

    variables = fs.load(file_suffix=file_suffix)
    return Output(file_suffix=file_suffix, variables=variables)

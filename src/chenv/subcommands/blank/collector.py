"""create a blank .env file."""
from typing import Optional

import click

from chenv.cli import cli
from chenv.models.output import Output

_DEFAULT_SUFFIX: str = "blank"


@cli.command(help="create a blank .env file")
@click.option("--name", "-n", help="File name suffix")
def blank(name: Optional[str]) -> Output:
    """Generate a blank `Output` instance."""
    return Output(file_suffix=name or _DEFAULT_SUFFIX, variables=dict())

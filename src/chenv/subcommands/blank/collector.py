"""create a blank .env file."""
from chenv.cli import cli
from chenv.models.output import Output


@cli.command(help="create a blank .env file")
def blank() -> Output:
    """Generate a blank `Output` instance."""
    return Output(file_suffix="blank", variables=dict())

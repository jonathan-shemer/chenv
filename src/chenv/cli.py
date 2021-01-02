"""Command-line interface."""
import click
from click.core import Context

from chenv import fs, settings, transform
from chenv.console import fatal
from chenv.models.output import Output, Target
from . import __version__

settings.load()


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version=__version__)
def cli(ctx: Context) -> None:
    """chenv. modern local environment management."""
    click.secho("chenv. modern local environment management", fg="green")
    if ctx.invoked_subcommand is None:
        import chenv.inputs

        ctx.invoke(chenv.inputs.local.collect)


@cli.resultcallback()
def _pipeline(result: Target) -> None:
    try:
        if isinstance(result, Output):
            transformed_output: Output = transform.apply(result)
            fs.assign_env(transformed_output)
        else:
            fs.force_link(result.filename)
        click.echo(
            f'{click.style(settings.DOTENV, fg="bright_black")}'
            f' → {click.style(result.filename, fg="bright_green")}'
        )
    except Exception as e:
        fatal(__name__, f"{e.__class__.__name__} - {str(e)}", 1)

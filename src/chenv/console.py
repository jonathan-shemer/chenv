"""user inteaction utilities."""
import os
from typing import NoReturn

import click
import questionary

from chenv import settings


def contextify(context: str, context_fg: str, message: str) -> str:
    """Add context prefix to messages."""
    return f"{click.style(context, fg=context_fg)} - {message}"


def info(context: str, message: str) -> None:
    """Echo info colored messages with context."""
    click.echo(contextify(context, "cyan", message))


def error(context: str, message: str) -> None:
    """Echo error colored messages with context."""
    click.echo(contextify(context, "red", message))


def fatal(context: str, message: str, exit_code: int) -> NoReturn:
    """Exit the program after echoing an error colored messages with context."""
    error(context, f'({click.style(str(exit_code), fg="yellow")}) - {message}')
    if 0 < exit_code < 126:
        exit(exit_code)

    raise ValueError("`exit_code` for `fatal` must be in range [1, 126).")


def get_env_or_prompt(context: str, key: str) -> str:
    """Get or promt user for chenv-specific environment variable."""
    try:
        return os.environ[key]
    except KeyError:
        pass

    ephasized_key = click.style(key, fg="yellow")
    info(context, f"Environment variable {ephasized_key} is not defined.")
    value = questionary.text("Define new value:", validate=bool).ask()
    if not value:
        raise ValueError(f"Cannot set value `{value}` to `{key}`")

    settings.add(key, value)
    settings.load()
    return value

"""user inteaction utilities."""
from enum import Enum
import os
from typing import NoReturn

import click
import questionary

from chenv import settings


class Color(Enum):
    """Colors for output.

    docs: https://click.palletsprojects.com/en/7.x/api/#click.style
    """

    BLACK = "black"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"
    BRIGHT_BLACK = "bright_black"
    BRIGHT_RED = "bright_red"
    BRIGHT_GREEN = "bright_green"
    BRIGHT_YELLOW = "bright_yellow"
    BRIGHT_BLUE = "bright_blue"
    BRIGHT_MAGENTA = "bright_magenta"
    BRIGHT_CYAN = "bright_cyan"
    BRIGHT_WHITE = "BRIGHT_WHITE"


def as_link(
    target: str,
    target_color: Color,
    source: str = settings.DOTENV,
    source_color: Color = Color.BRIGHT_BLACK,
) -> str:
    """Formart symlink relation, standardized, in color."""
    return (
        f"{click.style(source, fg=source_color.value)}"
        f" → {click.style(target, fg=target_color.value)}"
    )


def contextify(context: str, context_fg: Color, message: str) -> str:
    """Add context prefix to messages."""
    return f"{click.style(context, fg=context_fg.value)} - {message}"


def info(context: str, message: str) -> None:
    """Echo info colored messages with context."""
    click.echo(contextify(context, Color.CYAN, message))


def error(context: str, message: str) -> None:
    """Echo error colored messages with context."""
    click.echo(contextify(context, Color.RED, message))


def fatal(context: str, message: str, exit_code: int) -> NoReturn:
    """Exit the program after echoing an error colored messages with context."""
    error(
        context, f"({click.style(str(exit_code), fg=Color.YELLOW.value)}) - {message}"
    )
    if 0 < exit_code < 126:
        exit(exit_code)

    raise ValueError("`exit_code` for `fatal` must be in range [1, 126).")


def get_env_or_prompt(context: str, key: str) -> str:
    """Get or promt user for chenv-specific environment variable."""
    try:
        return os.environ[key]
    except KeyError:
        pass

    ephasized_key = click.style(key, fg=Color.YELLOW.value)
    info(context, f"Environment variable {ephasized_key} is not defined.")
    value = questionary.text("Define new value:", validate=bool).ask()
    if not value:
        raise ValueError(f"Cannot set value `{value}` to `{key}`")

    settings.add(key, value)
    settings.load()
    return value

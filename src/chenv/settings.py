"""general settings for the application."""
import os

from dotenv import load_dotenv

from chenv import fs

DOTENV: str = ".env"
PREFIX: str = f"{DOTENV}."
ENVMERGE: str = ".envmerge"
ENVIGNORE: str = ".envignore"


def _dotenv_path() -> str:
    return fs.local_file_path(DOTENV)


def mount() -> None:
    """Mount (load and set in current process) application variables from the local `.env` file."""
    load_dotenv(_dotenv_path())


def add(key: str, value: str) -> None:
    """Adds a new env-variable to the application's local `.env` file."""
    fs.dump(_dotenv_path(), {key: value}, overwrite=False)


def debug_mode() -> bool:
    """Returns whether `chenv` runs in debug mode."""
    return bool(os.getenv("DEBUG"))

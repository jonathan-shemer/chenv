"""general settings for the application."""
import os

from dotenv import load_dotenv

from chenv import fs

DOTENV = ".env"
PREFIX = f"{DOTENV}."


def filename_from_template(file_suffix: str) -> str:
    """Create full `.env`-style filename from `file_suffix`."""
    return f"{PREFIX}{file_suffix}"


def _dotenv_path() -> str:
    return os.path.join(os.path.dirname(__file__), ".env")


def load() -> None:
    """Load application variables from the local `.env` file."""
    load_dotenv(_dotenv_path())


def add(key: str, value: str) -> None:
    """Adds a new env-variable to the application's local `.env` file."""
    fs.append(_dotenv_path(), f"{key}={value}")

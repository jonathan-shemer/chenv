"""filesystem utilities."""
import os
from typing import Dict, Generator, Optional

from dotenv import dotenv_values, set_key

from chenv import settings


def filename_from_template(file_suffix: str) -> str:
    """Create full `.env`-style filename from `file_suffix`."""
    return f"{settings.PREFIX}{file_suffix}"


def local_file_path(filename: str) -> str:
    """Returns the full path of a local file."""
    return os.path.join(os.path.dirname(__file__), filename)


def load(*, path: Optional[str] = None, file_suffix: Optional[str] = None) -> dict:
    """Load application variables from a `.env` file at `path` or `file_suffix`."""
    if path is None and file_suffix is None:
        raise ValueError("Either `path` or `filename` must be defined, nither was.")

    if path is not None and file_suffix is not None:
        raise ValueError("Either `path` or `filename` must be defined, not both.")

    return dotenv_values(path or filename_from_template(file_suffix))  # type: ignore


def assign_env(filename: str, variables: Dict[str, str], overwrite: bool = True) -> None:
    """Dumps output as filename, then links .env to it."""
    dump(filename, variables, overwrite=overwrite)
    force_link(filename)


def dump(filename: str, variables: Dict[str, str], overwrite: bool) -> None:
    """Sets `variables` to the file at `filename`."""
    if overwrite:
        with open(filename, mode="w"):
            pass

    for key, value in variables.items():
        set_key(filename, key, value, quote_mode="never")  # type: ignore


def force_link(source_path: str) -> None:
    """Symlinks source_path to `.env`, forcibly."""
    try:
        os.remove(settings.DOTENV)
    except FileNotFoundError:
        pass

    os.symlink(source_path, settings.DOTENV)


def load_lines(file_path: str) -> Generator[str, None, None]:
    """Creates a generator for lines in `file_path`."""
    try:
        with open(file_path) as f:
            while line := f.readline():
                if line := line.strip():
                    yield line
    except FileNotFoundError:
        return

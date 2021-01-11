"""filesystem utilities."""
import os
from typing import Generator

from chenv.models.output import Output


def append(file_path: str, *line: str) -> None:
    """Append `line`(s) to the file at `file_path`."""
    with open(file_path, "a") as f:
        f.writelines(line)


def assign_env(output: Output) -> None:
    """Dumps output as f'.env.{file_suffix}' file, then links .env to it."""
    dump(output.filename, output.body)
    force_link(output.filename)


def dump(filename: str, body: str) -> None:
    """Writes body to the file at `file_path`."""
    with open(filename, "w") as f:
        f.write(body)


def force_link(source_path: str) -> None:
    """Symlinks source_path to `.env`, forcibly."""
    try:
        os.remove(".env")
    except FileNotFoundError:
        pass

    os.symlink(source_path, ".env")


def load_lines(file_path: str) -> Generator[str, None, None]:
    """Creates a generator for lines in `file_path`."""
    try:
        with open(file_path) as f:
            while (line := f.readline()) :
                if (line := line.strip()) :
                    yield line
    except FileNotFoundError:
        return

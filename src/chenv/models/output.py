"""declares outputs used to generate `.env`-style files."""
from dataclasses import dataclass
import os

from chenv import settings


@dataclass(frozen=True)
class Target:
    """Declares a target file to use as the `.env` file."""

    file_suffix: str

    @property
    def filename(self) -> str:  # noqa: ANN101
        """Generate a filename from this `Target` (by `file_suffix`)."""
        return settings.filename_from_template(self.file_suffix)


@dataclass(frozen=True)
class Output(Target):
    """Declares a target file, and body, to use as the `.env` file."""

    variables: dict

    @property
    def body(self) -> str:  # noqa: ANN101
        """Generate a file body from the `self.variables` dict."""
        return os.linesep.join(
            f"{key}={value}" for key, value in self.variables.items()
        )

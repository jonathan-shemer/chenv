"""declares outputs used to generate `.env`-style files."""
from dataclasses import dataclass
from typing import Dict

from chenv import fs


@dataclass(frozen=True)
class Output:
    """Declares a target file, and variables, to use as the `.env` file."""

    file_suffix: str
    variables: Dict[str, str]

    @property
    def filename(self) -> str:  # noqa: ANN101
        """Generate a filename from this `Target` (by `file_suffix`)."""
        return fs.filename_from_template(self.file_suffix)

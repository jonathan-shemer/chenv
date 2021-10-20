"""perform transformations on env-variables sets."""
from dataclasses import replace
from fnmatch import fnmatch

import toolz

from chenv import fs
from chenv import settings
from chenv.models.output import Output


def _ignore(variables: dict) -> dict:
    """Filter variable keys by unix patterns in `.envignore`."""
    ignores = set(fs.load_lines(settings.ENVIGNORE))
    return {key: value for key, value in variables.items() if not any(fnmatch(key, ignored) for ignored in ignores)}


def _merge(variables: dict) -> dict:
    """Merge / override variable set with env-variables defined in `.envmerge`."""
    overriders = fs.load(path=settings.ENVMERGE)
    return toolz.merge(variables, overriders)


def _escape(variables: dict) -> dict:
    r"""Replace new-lines with `\n` literal and escape using double-quotes."""

    def _escape_value(value: str) -> str:
        if value.isalnum():
            return value

        espaced_new_lines: str = value.replace("\n", "\\n")
        return f'"{espaced_new_lines}"'

    return toolz.valmap(_escape_value, variables)


def apply(output: Output) -> Output:
    """Apply all transformations to the `Output` set."""
    return replace(output, variables=toolz.pipe(output.variables, _ignore, _merge, _escape))

"""perform transformations on env-variables sets."""
from dataclasses import replace
from fnmatch import fnmatch

import toolz

from chenv import fs
from chenv import settings
from chenv.models.output import Output


def ignore(variables: dict) -> dict:
    """Filter variable keys by unix patterns in `.envignore`."""
    ignores = set(fs.load_lines(settings.ENVIGNORE))
    return {key: value for key, value in variables.items() if not any(fnmatch(key, ignored) for ignored in ignores)}


def merge(variables: dict) -> str:
    """Merge / override variable set with env-variables defined in `.envmerge`."""
    overriders = fs.load(path=settings.ENVMERGE)
    return toolz.merge(variables, overriders)


def apply(output: Output) -> Output:
    """Apply all transformations to the `Output` set."""
    return replace(output, variables=toolz.pipe(output.variables, ignore, merge))

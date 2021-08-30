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


def _new_lines(variables: dict) -> dict:
    r"""Replace new-lines with `\n` literal."""
    return toolz.valmap(lambda v: v.replace("\n", "\\n"), variables)


def apply(output: Output) -> Output:
    """Apply all transformations to the `Output` set."""
    return replace(output, variables=toolz.pipe(output.variables, _ignore, _merge, _new_lines))

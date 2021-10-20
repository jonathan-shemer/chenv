"""Test cases for the `transform` module."""
from contextlib import contextmanager
import os
from typing import Dict, Generator, List
from unittest.mock import patch
from uuid import uuid4

import pytest

from chenv.models.output import Output
import chenv.transform


@contextmanager
def _patch_ignore_patterns(patterns: List[str]) -> Generator:
    with patch("chenv.fs.load_lines", return_value=os.linesep.join(patterns)):
        yield


@contextmanager
def _patch_merge_variables(variables: Dict[str, str]) -> Generator:
    with patch("chenv.fs.load", return_value=variables):
        yield


@pytest.mark.parametrize(
    "variables, ignore, merge, expected",
    [
        (dict(), [], dict(), dict()),
        (dict(HELLO_1="world"), [], dict(), dict(HELLO_1="world")),
        (dict(HELLO_2="world\nEscaping"), [], dict(), dict(HELLO_2='"world\\nEscaping"')),
        (dict(HELLO_3="world"), ["HE*"], dict(), dict()),
        (dict(HELLO_4="world"), ["*LLO*"], dict(), dict()),
        (dict(HELLO_5="world"), ["*LLO*"], dict(HELLO="world"), dict(HELLO="world")),
        (dict(HELLO_6="world"), [], dict(HELLO_6="this is my world"), dict(HELLO_6='"this is my world"')),
    ],
)
def test_apply(variables: Dict[str, str], ignore: List[str], merge: Dict[str, str], expected: Dict[str, str]) -> None:
    """Test the functionality of `chenv.transform.apply`."""
    suffix: str = uuid4().hex
    base = Output(file_suffix=suffix, variables=variables)

    with _patch_ignore_patterns(ignore), _patch_merge_variables(merge):
        assert chenv.transform.apply(base) == Output(file_suffix=suffix, variables=expected)

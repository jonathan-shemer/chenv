"""Test cases for the `fs` module."""
from itertools import permutations
import os
import tempfile
from typing import Dict, Optional
from unittest.mock import patch

import pytest

import chenv.fs
import chenv.settings

_SAMPLE_FILE: str = "tests/samples/.env.sample"
_SAMPLE_VARIABLES: Dict[str, str] = dict(HELLO="world", CHENV="testing")


def test_filename_from_template() -> None:
    """Test `filename_from_template`."""
    assert chenv.fs.filename_from_template("hello") == ".env.hello"


@pytest.mark.parametrize("filename", ["hello", "world"])
def test_local_file_path(filename: str) -> None:
    """Test `local_file_path`."""
    with patch("os.path.dirname", return_value="/base/dir"):
        assert chenv.fs.local_file_path(filename) == f"/base/dir/{filename}"


def test_load_sample() -> None:
    """Test `local_file_path`."""
    assert chenv.fs.load(path=_SAMPLE_FILE) == _SAMPLE_VARIABLES


def test_load_parameters() -> None:
    """Test `local_file_path` parameter requirements."""
    with pytest.raises(ValueError):
        chenv.fs.load()


@pytest.mark.parametrize("overwrite", [False, True])
def test_assign_env(overwrite: bool) -> None:
    """Test `assign_env`."""
    with patch("chenv.fs.dump") as dump, patch("chenv.fs.force_link") as force_link:
        chenv.fs.assign_env(_SAMPLE_FILE, _SAMPLE_VARIABLES, overwrite=overwrite)
        dump.assert_called_once_with(_SAMPLE_FILE, _SAMPLE_VARIABLES, overwrite=overwrite)
        force_link.assert_called_once_with(_SAMPLE_FILE)


@pytest.mark.parametrize("overwrite, preexisting", permutations([False, True]))
def test_dump(overwrite: bool, preexisting: bool) -> None:
    """Test `dump`."""
    filename: str = ".env.dump"
    with tempfile.TemporaryDirectory() as dir:
        path: str = os.path.join(dir, filename)
        if preexisting:
            with open(path, "w") as f:
                # note: preexisting files must end with newline.
                f.write("INIT=true\n")

        if not (preexisting or overwrite):
            with pytest.raises(RuntimeError):
                chenv.fs.dump(path, _SAMPLE_VARIABLES, overwrite)
        else:
            chenv.fs.dump(path, _SAMPLE_VARIABLES, overwrite)
            with open(path) as f:
                content: str = f.read()
                assert content == ("INIT=true\n" if preexisting else "") + "HELLO=world\nCHENV=testing\n"


@pytest.mark.parametrize("preexisting", [False, True])
def test_force_link(preexisting: bool) -> None:
    """Test `force_link`."""
    filename: str = ".env.source"
    side_effect: Optional[Exception] = FileNotFoundError() if preexisting else None
    with patch("os.remove", side_effect=side_effect) as remove, patch("os.symlink") as symlink:
        chenv.fs.force_link(filename)
        remove.assert_called_once_with(chenv.settings.DOTENV)
        symlink.assert_called_once_with(filename, chenv.settings.DOTENV)


@pytest.mark.parametrize("path, expected", [(_SAMPLE_FILE, ["HELLO=world", 'CHENV="testing"']), (".env.missing", [])])
def test_load_lines(path: str, expected: Optional[Dict[str, str]]) -> None:
    """Test `load_lines`."""
    assert list(chenv.fs.load_lines(path)) == expected

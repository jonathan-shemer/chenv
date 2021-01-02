"""Test cases for the `console` module."""

from click.testing import CliRunner
import pytest


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()

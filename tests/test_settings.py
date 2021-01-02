"""Test cases for the `settings` module."""
from chenv import settings


def test_filename_from_template() -> None:
    """Test filename_from_template."""
    assert settings.filename_from_template("hello") == ".env.hello"

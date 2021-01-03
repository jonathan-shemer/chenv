"""Test cases for the `settings` module."""
import chenv.settings


def test_filename_from_template() -> None:
    """Test filename_from_template."""
    assert chenv.settings.filename_from_template("hello") == ".env.hello"

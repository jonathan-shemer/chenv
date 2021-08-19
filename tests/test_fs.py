"""Test cases for the `fs` module."""
import chenv.fs


def test_filename_from_template() -> None:
    """Test filename_from_template."""
    assert chenv.fs.filename_from_template("hello") == ".env.hello"

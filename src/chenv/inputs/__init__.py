"""implementation for difference sources of environment variables."""
from . import blank, heroku, local

__all__ = ["blank", "heroku", "local"]

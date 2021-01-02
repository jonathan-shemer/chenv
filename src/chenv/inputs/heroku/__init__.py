"""choose between remote config-vars, as defined in an heroku app."""
from .collector import heroku

__all__ = ["heroku"]

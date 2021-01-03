"""chenv. modern local environment management."""
from chenv import cli, settings

settings.load()


def main() -> None:
    """Main function / entry point for the application."""
    import chenv.inputs  # noqa: F401

    cli.cli()

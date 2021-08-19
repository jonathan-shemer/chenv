"""chenv. modern local environment management."""
from chenv import cli, settings

settings.mount()


def main() -> None:
    """Main function / entry point for the application."""
    from chenv import subcommands  # noqa: F401

    cli.cli()

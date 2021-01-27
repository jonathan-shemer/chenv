"""choose between remote config-vars, as defined in an heroku app."""
from functools import partial
import os
from typing import List, Optional

import click
import httpx
import questionary
from toolz import assoc, curry, dissoc, first, get_in, groupby

from chenv import console
from chenv.cli import cli
from chenv.models.output import Output

fatal = partial(console.fatal, __name__)


def _api_get(uri: str) -> httpx.Response:
    api_key = console.get_env_or_prompt(__name__, "HEROKU_API_KEY")
    return httpx.get(
        os.path.join("https://api.heroku.com", uri),
        headers=dict(
            Accept="application/vnd.heroku+json; version=3",
            Authorization=f"Bearer {api_key}",
        ),
    )


def _prompt_team_apps(default_team: Optional[str], apps: List[dict]) -> List[dict]:
    apps_by_team = groupby(curry(get_in, ["team", "name"]), apps)
    normalized_apps_by_team = dissoc(
        assoc(apps_by_team, "personal", apps_by_team[None]), None
    )

    if default_team and default_team in normalized_apps_by_team:
        team = default_team
    else:
        click.echo(
            f"""Teams found in account: {", ".join(sorted(
                click.style(team, fg="magenta")
                for team in normalized_apps_by_team))}"""
        )
        team = questionary.autocomplete(
            message="Choose team:", choices=normalized_apps_by_team
        ).ask()

    return normalized_apps_by_team[team]


def _prompt_app(default_app: Optional[str], apps: List[dict]) -> dict:
    apps_by_name = groupby("name", apps)
    if default_app and default_app in apps_by_name:
        name = default_app
    else:
        name = questionary.autocomplete(
            message="Choose app:", choices=apps_by_name
        ).ask()

    return first(apps_by_name[name])


def _choose_app(default_team: Optional[str], default_app: Optional[str]) -> dict:
    response = _api_get("apps")
    team_apps = _prompt_team_apps(default_team, response.json())
    return _prompt_app(default_app, team_apps)


def _get_config_vars(app: dict) -> dict:
    response = _api_get(f'apps/{app["id"]}/config-vars')
    return response.json()


@cli.command(help="choose between remote config-vars, as defined in an heroku app")
@click.option("--team", "-t", help="Heroku team name")
@click.option("--app", "-a", help="Heroku app name in the team")
def heroku(team: Optional[str], app: Optional[str]) -> Output:
    """Choose between remote config-vars, as defined in an heroku app."""
    chosen_app = _choose_app(team, app)
    vars = _get_config_vars(chosen_app)
    return Output(variables=vars, file_suffix=chosen_app["name"])

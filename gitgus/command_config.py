import os.path
from enum import Enum

import toml
import typer
from rich import print
from rich.prompt import Prompt

from gitgus.config import DEFAULT_CONFIG_PATH, Config
from gitgus.deps import config, teams, products
from gitgus.utils.console_input import choose_one

config_app = typer.Typer(no_args_is_help=True)


class ConfigLocation(str, Enum):
    glob = "global"
    local = "local"


@config_app.command()
def init(location: ConfigLocation = typer.Argument(..., help="Initialize a local or global config file?")):
    """Initialize the config file."""
    local = location == ConfigLocation.local
    init_config = Config()
    init_config.load_defaults()

    if not local:
        init_config.load_global_init_values()

    if local:
        # GUS config
        team = choose_one(
            "What is your GUS Team Name? (partial okay)",
            search_fn=lambda n: teams.get_team(n),
        )
        if team:
            init_config.set("GUS.default_team", team.id_)

        product_tag = choose_one(
            "What is your GUS Product Tag ID?",
            search_fn=lambda n: products.get_product_tag(n),
        )
        if product_tag:
            init_config.set("GUS.default_product_tag", product_tag.id_)

        # Github config
        team_prefix = Prompt.ask(
            "What is your GitHub team prefix? eg. gears, ops, accel", default=config.get("PRs.team_prefix")
        )
        if team_prefix:
            init_config.set("PRs.team_prefix", team_prefix)

    github_token = Prompt.ask(
        "What is your GitHub token? see: https://tinyurl.com/3u93asa4 Remember to config SSO and permissions."
        "Leave blank to skip.",
        default="",
    )
    if github_token:
        init_config.set_secret("github.token", github_token)

    if local:
        path = os.path.join(os.getcwd(), ".gitgus.toml")
    else:
        path = DEFAULT_CONFIG_PATH
    init_config.write(path)
    print(f"Wrote config to default file {path}.")
    if not local:
        print(
            "Please initialize a local config file with `gitgus config init local` in your project directory to "
            "setup GUS and GH values."
        )


@config_app.command()
def write():
    """Write the current config to file."""
    config.write(None)
    print(f"Wrote config to default file {DEFAULT_CONFIG_PATH}.")


@config_app.command()
def get(name: str = typer.Argument(..., help="The name of the config value to get")):
    """Read the current config from file."""
    if name is None:
        val = config.all()
    else:
        val = config.get(name)
    if isinstance(val, dict):
        print(toml.dumps(config.get(name)))
    else:
        print(val)


@config_app.command()
def set(
    name: str = typer.Argument(..., help="The name of the config value to set"),
    value: str = typer.Argument(..., help="The value to set the config value to"),
):
    """Read the current config from file."""
    config.set(name, value)
    config.write(None)
    print(f"Set [bold red]{name}[/bold red] to [bold blue]{value}[/bold blue].")
    print(f"Wrote config to default file {DEFAULT_CONFIG_PATH}.")

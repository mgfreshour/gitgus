import os.path
from enum import Enum

import toml
import typer
from rich import print
from rich.prompt import Prompt

from gitgus.config import DEFAULT_CONFIG_PATH, Config
from gitgus.deps import config, products
from gitgus.utils.console_input import choose_one
from gitgus.gus.sobjects.team import Team
from gitgus.gus.sobjects.product_tag import ProductTag
from gitgus.oauth.device import get_auth_token as get_auth_token_device

config_app = typer.Typer(no_args_is_help=True)


class ConfigLocation(str, Enum):
    glob = "global"
    local = "local"


def get_github_token() -> str:
    base_url = "https://github.com"
    device_uri = base_url + "/login/device/code"
    token_url = base_url + "/login/oauth/access_token"

    def get_code(code, url):
        print(f"Go to {url} and enter code {code}")

    return get_auth_token_device(device_uri, token_url, "0df336fe16abeebc0aa7", ["repo", "project", "user"], get_code)


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
            search_fn=lambda n: Team.find_by_name_like(n),
            default=config.get("GUS.default_team"),
        )
        if team:
            init_config.set("GUS.default_team", (team.name, team.id_))

        product_tag = choose_one(
            "What is your GUS Product Tag ID?",
            search_fn=lambda n: ProductTag.find_by_name_like(n),
            default=config.get("GUS.default_product_tag"),
        )
        if product_tag:
            init_config.set("GUS.default_product_tag", (product_tag.name, product_tag.id_))

        # Github config
        team_prefix = Prompt.ask(
            "What is your GitHub team prefix? eg. gears, ops, accel", default=config.get("PRs.team_prefix")
        )
        if team_prefix:
            init_config.set("PRs.team_prefix", team_prefix)

    gh_yn = Prompt.ask(
        f"Do you wish to setup a GitHub token? ({config.get('github.token')})", choices=["Y", "N"], default="Y"
    )
    if gh_yn == "Y":
        gh_token = get_github_token()
        init_config.set_secret("github.token", gh_token)

    current_jenkins_url = config.get("jenkins.url")
    current_jenkins_user = config.get("jenkins.username")
    jenkins_yn = Prompt.ask(
        f"Do you wish to setup a Jenkins token? ({current_jenkins_user}@{current_jenkins_url}",
        choices=["Y", "N"],
        default="Y",
    )
    if jenkins_yn == "Y":
        jenkins_url = Prompt.ask("What is your Jenkins URL?", default=current_jenkins_url)
        jenkins_user = Prompt.ask("What is your Jenkins username?", default=current_jenkins_user)
        jenkins_password = Prompt.ask(
            "What is your Jenkins API Token? (go to Jenkins -> Your Name -> Configure -> Configure -> API Token",
            default=config.get("jenkins.password"),
        )
        init_config.set("jenkins.url", jenkins_url)
        init_config.set("jenkins.username", jenkins_user)
        init_config.set_secret("jenkins.password", jenkins_password)

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

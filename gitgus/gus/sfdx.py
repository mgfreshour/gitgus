"""Client for sfdx CLI."""

from datetime import datetime, timedelta
from json import loads, dumps

from rich import print
from rich.console import Console
from typer import Exit

from gitgus.utils.secret_store import get_secret, set_secret


def auth_web_login(instance: str):
    """
    Run sfdx auth:web:login.

    :param instance: Salesforce instance (gus.my.salesforce.com)
    :returns: auth connections
    :raises Exit: if sfdx cli isn't installed
    """
    try:
        from sh import sfdx
    except ImportError:
        print(  # noqa: T001 T201
            "[bold red]sfdx CLI is not installed[/bold red]\n"
            "https://developer.salesforce.com/tools/sfdxcli\n"
            "[bold]install with brew: [yellow]brew install --cask sfdx[/yellow][/bold]"
        )
        raise Exit(1)

    with Console().status("Logging in with web browser", spinner="point"):
        res = sfdx(
            "force:auth:web:login",
            "--instanceurl",
            f"https://{instance}",
            "--json",
            _tty_out=False,
        )
        return loads(res)["result"]


def get_session_id(instance: str, max_age_hours: int = 8) -> str:
    """
    Get Salesforce session id.

    :param instance: Salesforce instance (gus.my.salesforce.com)
    :param max_age_hours: max age for session id
    :returns: session id
    """
    sfdx_cache = get_secret("sfdx-cache", instance)
    cache = loads(sfdx_cache) if sfdx_cache else None
    if cache and datetime.fromisoformat(cache["time_collected"]) > datetime.utcnow() - timedelta(hours=max_age_hours):
        return cache["access_token"]
    else:
        token = auth_web_login(instance)["accessToken"]
        cache = {
            "time_collected": datetime.utcnow().isoformat(),
            "access_token": token,
        }
        set_secret("sfdx-cache", instance, dumps(cache))
        return token

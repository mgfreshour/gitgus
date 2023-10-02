from datetime import datetime, timedelta
from json import loads, dumps

from gitgus.utils.secret_store import get_secret, set_secret
from gitgus.oauth.pkce import get_auth_token


def get_session_token(instance: str, max_age_hours: int = 8) -> str:
    """
    Get Salesforce session id.

    :param instance: Salesforce instance (gus.my.salesforce.com)
    :param max_age_hours: max age for session id
    :returns: session id
    """
    sfdx_cache = get_secret("sfdx-cache", instance)
    cache = loads(sfdx_cache) if sfdx_cache else None
    if cache and datetime.fromisoformat(
        cache["time_collected"]
    ) > datetime.utcnow() - timedelta(hours=max_age_hours):
        return cache["access_token"]
    else:
        base_url = "https://gus.my.salesforce.com"
        auth_url = base_url + "/services/oauth2/authorize?"
        token_url = base_url + "/services/oauth2/token"
        token = get_auth_token(
            auth_url, token_url, "PlatformCLI", ["refresh_token api web"]
        )
        cache = {
            "time_collected": datetime.utcnow().isoformat(),
            "access_token": token,
        }
        set_secret("sfdx-cache", instance, dumps(cache))
        return token

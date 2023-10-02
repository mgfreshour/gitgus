import pytest

from gitgus.oauth.pkce import get_auth_token as get_auth_token_pkce
from gitgus.oauth.device import get_auth_token as get_auth_token_device


@pytest.mark.skip(reason="requires manual testing")
def test_get_auth_token_gus():
    token = get_auth_token_pkce(
        "https://gus.my.salesforce.com", "PlatformCLI", ["refresh_token api web"]
    )
    assert token
    print(token)


@pytest.mark.skip(reason="requires manual testing")
def test_get_auth_token_github(capsys):
    base_url = "https://github.com"
    device_uri = base_url + "/login/device/code"
    token_url = base_url + "/login/oauth/access_token"

    def get_code(code, url):
        with capsys.disabled():
            print(f"Go to {url} and enter code {code}")

    token = get_auth_token_device(
        device_uri,
        token_url,
        "0df336fe16abeebc0aa7",
        ["repo", "project", "user"],
        get_code,
    )
    assert token
    print(token)

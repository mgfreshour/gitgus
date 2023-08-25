from time import sleep
from typing import Callable

import requests


def get_auth_token(device_uri, token_uri, client_id, scopes: list[str], code_getter: Callable[[str, str], None]):
    device_code, user_code, code_url, expires_in = get_verification_code(device_uri, client_id, scopes)
    code_getter(code_url, user_code)
    return poll_for_auth(token_uri, device_code, client_id, expires_in)


def get_verification_code(device_uri, client_id, scopes: list[str]):
    data = {"client_id": client_id, "scope": " ".join(scopes)}
    resp = requests.post(device_uri, data=data, headers={"Accept": "application/json"})
    if resp.status_code != 200:
        raise RuntimeError(f"Error: no authorization code returned from browser: {resp.text}")
    payload = resp.json()
    return payload["device_code"], payload["user_code"], payload["verification_uri"], payload["expires_in"]


def poll_for_auth(token_uri, device_code, client_id, expires_in: int):
    grant_type = "urn:ietf:params:oauth:grant-type:device_code"
    data = {"grant_type": grant_type, "device_code": device_code, "client_id": client_id}
    max_retries = expires_in // 30 - 1
    while max_retries > 0:
        resp = requests.post(token_uri, data=data, headers={"Accept": "application/json"})
        max_retries -= 1
        payload = resp.json()
        if "access_token" in payload:
            return payload["access_token"]
        sleep(30)
    raise RuntimeError("Error: no authorization code returned from service")

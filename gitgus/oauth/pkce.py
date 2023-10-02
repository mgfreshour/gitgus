import base64
import hashlib
import string
from http.server import BaseHTTPRequestHandler, HTTPServer
from random import SystemRandom
from urllib import parse

import requests

PORT = 1717

redirect_url = "http://localhost:1717/OauthRedirect"


class OAuthHttpServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        self.authorization_code = ""


class OAuthHttpHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress logging

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(
            '<script type="application/javascript">window.close();</script>'.encode(
                "UTF-8"
            )
        )

        parsed = parse.urlparse(self.path)
        qs = parse.parse_qs(parsed.query)

        self.server.authorization_code = qs["code"][0]


def get_auth_token(auth_uri, token_uri, client_id, scopes: list[str]):
    code_verifier = create_code_verifier()
    code_challenge = create_code_challenge(code_verifier)
    auth_url = create_auth_url(code_challenge, auth_uri, client_id, scopes)
    open_auth_url(auth_url)
    authorization_code = start_web_server()
    access_token = get_access_token(
        authorization_code, code_verifier, client_id, token_uri
    )
    return access_token


def create_code_verifier():
    rand = SystemRandom()
    code_verifier = "".join(rand.choices(string.ascii_letters + string.digits, k=128))
    return code_verifier


def create_code_challenge(code_verifier):
    code_sha_256 = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    b64 = base64.urlsafe_b64encode(code_sha_256)
    code_challenge = b64.decode("utf-8").replace("=", "")
    return code_challenge


def start_web_server():
    server_address = ("localhost", PORT)
    httpd = OAuthHttpServer(server_address, OAuthHttpHandler)
    httpd.timeout = 120
    httpd.handle_request()
    authorization_code = httpd.authorization_code
    httpd.server_close()
    if authorization_code == "":
        raise RuntimeError("Error: no authorization code returned from browser")
    return authorization_code


def create_auth_url(code_challenge, auth_url, client_id, scopes: list[str]):
    auth_url = (
        auth_url
        + "response_type=code&client_id="
        + client_id
        + "&scope="
        + "+".join(scopes)
        + f"&redirect_uri={redirect_url}&"
        + "code_challenge="
        + code_challenge
        + "&code_challenge_method=S256"
    )
    return auth_url


def open_auth_url(auth_url):
    import webbrowser

    webbrowser.open(auth_url)


def get_access_token(authorization_code, code_verifier, client_id, token_uri):
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_url,
        "client_id": client_id,
        "code_verifier": code_verifier,
    }

    response = requests.post(token_uri, data=data)

    if response.status_code != 200:
        raise RuntimeError(
            f"Error: no authorization code returned from browser: {response.text}"
        )
    try:
        access_token = response.json()["access_token"]
    except Exception as e:
        raise RuntimeError(f"Error: no authorization code returned from browser: {e}")

    return access_token

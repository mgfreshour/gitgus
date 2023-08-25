import builtins
import os
from unittest.mock import mock_open, MagicMock

import toml

from gitgus.config import Config, DEFAULT_CONFIG_PATH, IS_SECRET_TOKEN

PARTIAL_CONFIG = """
[PRs]
body_template = ".github/PULL_REQUEST_TEMPLATE.md"
team_prefix = "not_myteam"
"""


def test_set_secret(monkeypatch):
    mock_secret = MagicMock()
    monkeypatch.setattr("gitgus.config.set_secret", mock_secret)
    testee = Config()
    testee.load_defaults()
    testee.set_secret("jenkins.password", "mysecret")
    assert testee.all()["jenkins"]["password"] == IS_SECRET_TOKEN
    assert mock_secret.call_count == 1
    assert mock_secret.call_args[0][1] == "jenkins.password"
    assert mock_secret.call_args[0][2] == "mysecret"


def test_loads_local_config(fs):
    fs.create_file("/foo/bar/.gitgus.toml", contents=PARTIAL_CONFIG)
    os.chdir("/foo/bar")
    config = Config()
    config.load()
    assert config.get("PRs.body_template") == ".github/PULL_REQUEST_TEMPLATE.md"
    assert config.get("PRs.team_prefix") == "not_myteam"


def test_loads_local_config_from_parent(fs):
    fs.create_file("/foo/bar/.gitgus.toml", contents=PARTIAL_CONFIG)
    fs.create_dir("/foo/bar/baz/bat")
    os.chdir("/foo/bar/baz/bat")
    config = Config()
    config.load()
    assert config.get("PRs.body_template") == ".github/PULL_REQUEST_TEMPLATE.md"
    assert config.get("PRs.team_prefix") == "not_myteam"


def test_loads_global_config(fs):
    fs.create_file(DEFAULT_CONFIG_PATH, contents=PARTIAL_CONFIG)
    config = Config()
    config.load()
    assert config.get("PRs.body_template") == ".github/PULL_REQUEST_TEMPLATE.md"
    assert config.get("PRs.team_prefix") == "not_myteam"


def test_get_dots():
    config = Config()
    config.load_defaults()
    config.load_global_init_values()
    assert config.get("PRs.body_template") == ".github/PULL_REQUEST_TEMPLATE.md"
    assert config.get("PRs.queries.default") == "is:open repo:${repo} head:${team_prefix}"


def test_set_dots(monkeypatch):
    config = Config()
    config.load_defaults()
    config.set("PRs.body_template", "foo")
    assert config.get("PRs.body_template") == "foo"
    config.set("PRs.queries.default", "bar")
    assert config.get("PRs.queries.default") == "bar"


def test_write(monkeypatch):
    config = Config()
    config.load_defaults()
    m = mock_open()
    monkeypatch.setattr(builtins, "open", m)
    config.write(None)
    m.assert_called_once_with(DEFAULT_CONFIG_PATH, "w")
    m().write.assert_called_once_with(toml.dumps(config.all()))

import builtins
import os
from unittest.mock import mock_open, MagicMock

import toml
from typer.testing import CliRunner

from gitgus.deps import config
from gitgus.config import DEFAULT_CONFIG_PATH
from gitgus.command_config import config_app, Config
from gitgus.gus.sobjects.sobject_base import SObjectBase
from gitgus.gus.sobjects.team import Team
from gitgus.gus.sobjects.product_tag import ProductTag


# def test_init_all_defaults(monkeypatch):
#     m = mock_open()
#     monkeypatch.setattr(builtins, "open", m)
#     runner = CliRunner()
#     result = runner.invoke(config_app, ["init"], input="\n\n\n")
#     assert result.exit_code == 0
#     assert "Wrote config to default file" in result.stdout
#     m.assert_called_once_with(DEFAULT_CONFIG_PATH, "w")


def test_write(monkeypatch):
    m = mock_open()
    monkeypatch.setattr(builtins, "open", m)
    runner = CliRunner()
    result = runner.invoke(config_app, ["write"])
    assert result.exit_code == 0
    assert "Wrote config to default file" in result.stdout
    m.assert_called_once_with(DEFAULT_CONFIG_PATH, "w")


def test_get():
    config.load_global_init_values()
    runner = CliRunner()
    result = runner.invoke(config_app, ["get", "GUS.style.work_id"])
    assert result.exit_code == 0
    assert "bold red" in result.stdout


def test_set(monkeypatch):
    m = mock_open()
    monkeypatch.setattr(builtins, "open", m)
    runner = CliRunner()
    result = runner.invoke(config_app, ["set", "GUS.default_team", "foo"])
    assert result.exit_code == 0
    assert "Wrote config to default file" in result.stdout
    result = runner.invoke(config_app, ["get", "GUS.default_team"])
    assert result.exit_code == 0
    assert config._config["GUS"]["default_team"] == "foo"


def assert_file_written(m, config_path):
    m.assert_called_once_with(config_path, "w")
    write_calls = [call for call in m.mock_calls if call[0] == "().write"]
    assert len(write_calls) == 1
    payload = toml.loads(write_calls[0][1][0])
    return payload


def test_init_global(monkeypatch):
    m = mock_open()
    monkeypatch.setattr(builtins, "open", m)
    monkeypatch.setattr(Config, "set_secret", MagicMock())

    runner = CliRunner()
    input = ["myghtoken"]
    result = runner.invoke(config_app, ["init", "global"], input="\n".join(input))

    assert result.exit_code == 0, result.stdout
    assert_file_written(m, DEFAULT_CONFIG_PATH)
    assert "Wrote config to default file" in result.stdout
    assert Config.set_secret.call_count == 1
    assert Config.set_secret.call_args[0][0] == "github.token"
    assert Config.set_secret.call_args[0][1] == "myghtoken"


def test_init_local(monkeypatch, capsys):
    def fake_soql_query(query):
        if "myteam" in query:
            return [Team.model_construct(id_="123", name="myteam")]
        if "myproduct" in query:
            return [ProductTag.model_construct(id_="456", name="myproduct")]
        return []

    m = mock_open()
    monkeypatch.setattr(builtins, "open", m)
    monkeypatch.setattr(Config, "set_secret", MagicMock())
    monkeypatch.setattr(Team, "soql_query", MagicMock(side_effect=fake_soql_query))
    monkeypatch.setattr(ProductTag, "soql_query", MagicMock(side_effect=fake_soql_query))
    monkeypatch.setattr(SObjectBase, "_query_soql", MagicMock(side_effect=RuntimeError("should not be called")))

    runner = CliRunner()
    input = ["myteam", "myproduct", "myprefix", "", ""]  # github token
    result = runner.invoke(config_app, ["init", "local"], input="\n".join(input))

    with capsys.disabled():
        print(result.stdout)

    assert result.exit_code == 0, result.stdout
    payload = assert_file_written(m, os.path.join(os.getcwd(), ".gitgus.toml"))
    assert payload["GUS"]["default_team"] == ["myteam", "123"]
    assert payload["GUS"]["default_product_tag"] == ["myproduct", "456"]
    assert payload["PRs"]["team_prefix"] == "myprefix"

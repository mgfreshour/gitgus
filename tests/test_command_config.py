import builtins
from unittest.mock import mock_open

from typer.testing import CliRunner

from gitgus.deps import config
from gitgus.config import DEFAULT_CONFIG_PATH
from gitgus.command_config import config_app


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

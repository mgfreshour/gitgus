from unittest.mock import MagicMock

from gitgus import command_gus
from typer.testing import CliRunner

from tests.testing_utils import create_wi


def test_list_no_args(monkeypatch):
    mock_gus_list = MagicMock()
    monkeypatch.setattr("gitgus.command_gus.GusWorkflow.query", mock_gus_list)
    mock_gus_list.return_value = [
        create_wi("W-1234", "Hello World"),
        create_wi("W-5678", "Goodbye World"),
    ]
    runner = CliRunner(env={"COLUMNS": "200", "ROWS": "24"})
    result = runner.invoke(command_gus.gus_app, ["list"])
    mock_gus_list.assert_called_with("default")
    assert result.exit_code == 0
    assert "W-1234" in result.stdout
    assert "W-5678" in result.stdout


def test_list_with_args(monkeypatch):
    mock_gus_list = MagicMock()
    monkeypatch.setattr("gitgus.command_gus.GusWorkflow.query", mock_gus_list)
    mock_gus_list.return_value = [
        create_wi("W-1234", "Hello World"),
        create_wi("W-5678", "Goodbye World"),
    ]
    runner = CliRunner(env={"COLUMNS": "200", "ROWS": "24"})
    result = runner.invoke(command_gus.gus_app, ["list", "mine"])
    mock_gus_list.assert_called_with("mine")
    assert result.exit_code == 0
    assert "W-1234" in result.stdout
    assert "W-5678" in result.stdout


def test_checkout_no_options(monkeypatch):
    mock_gus_co = MagicMock()
    monkeypatch.setattr("gitgus.command_gus.GusWorkflow.checkout", mock_gus_co)
    mock_gus_co.return_value = [
        "W-1234-branch",
        create_wi("W-1234", "Hello World"),
    ]
    runner = CliRunner()
    result = runner.invoke(command_gus.gus_app, ["checkout"])
    assert result.exit_code == 0
    assert "Checked out W-1234-branch" in result.stdout


def test_checkout_with_ip_option(monkeypatch):
    mock_gus_co = MagicMock()
    monkeypatch.setattr("gitgus.command_gus.GusWorkflow.checkout", mock_gus_co)
    mock_gus_co.return_value = [
        "W-1234-branch",
        create_wi("W-1234", "Hello World"),
    ]
    runner = CliRunner()
    result = runner.invoke(command_gus.gus_app, ["checkout", "--ip"])
    assert result.exit_code == 0
    assert "Checked out W-1234-branch" in result.stdout
    assert "Ticket marked as in progress" in result.stdout

from unittest.mock import MagicMock

from typer.testing import CliRunner
from gitgus.command_pr import pr_app
from tests.testing_utils import create_pr, create_wi


def test_create(monkeypatch):
    mock_prs_create = MagicMock()
    monkeypatch.setattr("gitgus.command_pr.PrWorkflow.create", mock_prs_create)
    mock_prs_create.return_value = create_pr("W-1234"), create_wi("W-1234")
    runner = CliRunner()
    result = runner.invoke(pr_app, ["create"])
    mock_prs_create.assert_called_with(draft=False, rfr=True, assign=True)
    assert result.exit_code == 0
    assert "W-1234" in result.stdout


def test_query_default(monkeypatch):
    mock_prs_list = MagicMock()
    monkeypatch.setattr("gitgus.command_pr.PrWorkflow.list_prs", mock_prs_list)
    mock_prs_list.return_value = [
        create_pr("W-1234"),
        create_pr("W-5678"),
    ]
    runner = CliRunner()
    result = runner.invoke(pr_app, ["query", "default"])
    mock_prs_list.assert_called_with("default")
    assert result.exit_code == 0
    assert "W-1234" in result.stdout
    assert "W-5678" in result.stdout


def test_query_argument(monkeypatch):
    mock_prs_list = MagicMock()
    monkeypatch.setattr("gitgus.command_pr.PrWorkflow.list_prs", mock_prs_list)
    mock_prs_list.return_value = [
        create_pr("W-1234"),
        create_pr("W-5678"),
    ]
    runner = CliRunner()
    result = runner.invoke(pr_app, ["query", "bobo"])
    mock_prs_list.assert_called_with("bobo")
    assert result.exit_code == 0
    assert "W-1234" in result.stdout
    assert "W-5678" in result.stdout


def test_mine(monkeypatch):
    mock_prs_list = MagicMock()
    monkeypatch.setattr("gitgus.command_pr.PrWorkflow.list_prs", mock_prs_list)
    mock_prs_list.return_value = [
        create_pr("W-1234"),
        create_pr("W-5678"),
    ]
    runner = CliRunner()
    result = runner.invoke(pr_app, ["mine"])
    mock_prs_list.assert_called_with("mine")
    assert result.exit_code == 0
    assert "W-1234" in result.stdout
    assert "W-5678" in result.stdout


def test_list(monkeypatch):
    mock_prs_list = MagicMock()
    monkeypatch.setattr("gitgus.command_pr.PrWorkflow.list_prs", mock_prs_list)
    mock_prs_list.return_value = [
        create_pr("W-1234"),
        create_pr("W-5678"),
    ]
    runner = CliRunner()
    result = runner.invoke(pr_app, ["list"])
    mock_prs_list.assert_called_with("default")
    assert result.exit_code == 0
    assert "W-1234" in result.stdout
    assert "W-5678" in result.stdout

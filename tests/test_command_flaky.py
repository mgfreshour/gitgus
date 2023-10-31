from datetime import datetime
from unittest.mock import MagicMock

import pytest

from gitgus.command_flaky import flaky_app
from typer.testing import CliRunner

from gitgus.gus.sobjects.work import Work
from gitgus.gus.gus_client import GUSClient
from tests.testing_utils import create_wi

from gitgus.deps import config


@pytest.fixture(autouse=True)
def _before(monkeypatch):
    config.load_global_init_values()
    monkeypatch.setattr(GUSClient, "_connect_gus_with_sso", MagicMock())


def test_create_no_options(monkeypatch):
    monkeypatch.setattr(Work, "create", MagicMock())
    mock_get_job_name = MagicMock()
    monkeypatch.setattr(
        "gitgus.workflows.flaky_wf.FlakyWorkflow._get_job_name", mock_get_job_name
    )
    mock_get_job_name.return_value = "funhouse"
    mock_get_test_stacktrace = MagicMock()
    monkeypatch.setattr(
        "gitgus.workflows.flaky_wf.FlakyWorkflow._get_test_stacktrace",
        mock_get_test_stacktrace,
    )
    mock_get_test_stacktrace.return_value = "stacktrace", "test_name"
    runner = CliRunner()
    result = runner.invoke(flaky_app, ["create-tickets"], input="123\n")
    assert result.exit_code == 0, result.stdout
    assert "Created ticket to disable" in result.stdout
    assert "Created ticket to fix" in result.stdout
    wi1 = Work.create.call_args_list[0].kwargs
    assert wi1["subject"] == "[Flaky Test] - Disable test: test_name"
    assert wi1["priority"] == "P2"
    wi2 = Work.create.call_args_list[1].kwargs
    assert wi2["subject"] == "[Flaky Test] - Fix test_name"
    assert wi2["priority"] == "P2"


def test_create_with_options(monkeypatch):
    monkeypatch.setattr(Work, "create", MagicMock())
    mock_get_job_name = MagicMock()
    monkeypatch.setattr(
        "gitgus.workflows.flaky_wf.FlakyWorkflow._get_job_name", mock_get_job_name
    )
    mock_get_job_name.return_value = "funhouse"
    mock_get_test_stacktrace = MagicMock()
    monkeypatch.setattr(
        "gitgus.workflows.flaky_wf.FlakyWorkflow._get_test_stacktrace",
        mock_get_test_stacktrace,
    )
    mock_get_test_stacktrace.return_value = "stacktrace", "test_name"
    runner = CliRunner()
    result = runner.invoke(flaky_app, ["create-tickets", "--build", "123"])
    assert result.exit_code == 0, result.stdout
    assert "Created ticket to disable" in result.stdout
    assert "Created ticket to fix" in result.stdout
    wi1 = Work.create.call_args_list[0].kwargs
    assert wi1["subject"] == "[Flaky Test] - Disable test: test_name"
    assert wi1["priority"] == "P2"
    wi2 = Work.create.call_args_list[1].kwargs
    assert wi2["subject"] == "[Flaky Test] - Fix test_name"
    assert wi2["priority"] == "P2"


def test_report_all_builds(monkeypatch):
    mock_report = MagicMock()
    monkeypatch.setattr(
        "gitgus.workflows.flaky_wf.FlakyWorkflow.build_report", mock_report
    )
    mock_report.return_value = ({}, {})
    runner = CliRunner()
    result = runner.invoke(
        flaky_app,
        [
            "report-all-builds",
            "bobo/jobs",
            "--start-date",
            "2021-01-01",
            "--end-date",
            "2021-01-02",
        ],
    )
    assert result.exit_code == 0, result.stdout + result.stderr
    # Assert inclusive dates
    mock_report.assert_called_once_with(
        "bobo/jobs", datetime(2021, 1, 1, 0, 0), datetime(2021, 1, 2, 23, 59, 59)
    )
    # TODO: assert output


def test_report(monkeypatch):
    mock_report = MagicMock()
    mock_report.return_value = ({}, 12)
    mock_get_flaky_tagged_tests = MagicMock()
    monkeypatch.setattr("gitgus.workflows.flaky_wf.FlakyWorkflow.report", mock_report)
    monkeypatch.setattr(
        "gitgus.workflows.flaky_wf.FlakyWorkflow.get_flaky_tagged_tests",
        mock_get_flaky_tagged_tests,
    )
    runner = CliRunner()
    result = runner.invoke(
        flaky_app,
        [
            "report-failed-builds",
            "bobo/jobs",
            "--start-date",
            "2021-01-01",
            "--end-date",
            "2021-01-02",
        ],
    )
    assert result.exit_code == 0, result.stdout
    # Assert inclusive dates
    mock_report.assert_called_once_with(
        "bobo/jobs", datetime(2021, 1, 1, 0, 0), datetime(2021, 1, 2, 23, 59, 59)
    )
    # TODO: assert output

import os
from typing import Any
from unittest.mock import MagicMock

import builtins
from unittest.mock import mock_open

import pytest

from gitgus.config import Config
from gitgus.workflows.prs_wf import PrWorkflow
from gitgus.gus.sobjects.work import Work
from tests.testing_utils import create_wi

EDIT_RETURN = "Descriptions"
BRANCH_NAME = "myteam/@W-1234@-test"
REPO_NAME = "myteam/awesome"
WI_SUBJECT = "Hello World"
WI_BODY = "This is a test"

testee: PrWorkflow
mock_config: MagicMock
mock_edit: MagicMock
mock_gh: MagicMock
mock_git_repo: MagicMock
mock_workitems: MagicMock
mock_jenki: MagicMock


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
    global testee, mock_config, mock_edit, mock_gh, mock_git_repo, mock_workitems
    mock_config = Config()
    mock_config._config = {
        "PRs": {
            "body_template": ".github/PULL_REQUEST_TEMPLATE.md",
            "team_prefix": "myteam",
        }
    }
    mock_gh = MagicMock()
    mock_gh.get_repos.return_value = []
    mock_git_repo = MagicMock()
    mock_git_repo.get_branch_name.return_value = BRANCH_NAME
    mock_git_repo.get_repo_name.return_value = REPO_NAME
    mock_workitems = MagicMock()
    mock_edit = MagicMock()
    mock_jenki = MagicMock()
    mock_edit.edit.return_value = EDIT_RETURN
    wi = create_wi("W-1234", WI_SUBJECT, WI_BODY)
    mock_workitems.get_work_item.return_value = wi

    monkeypatch.setattr(Work, "get_by_name", lambda x: wi)

    testee = PrWorkflow(
        mock_config, mock_gh, mock_git_repo, mock_workitems, mock_edit, mock_jenki
    )
    monkeypatch.setattr(testee, "_read_body_template", lambda: "Bobobobob")
    monkeypatch.setattr(testee, "_has_commits_against_master", lambda: True)


def test_create_pushes_first(monkeypatch):
    testee.create()
    mock_git_repo.push.assert_called_once_with()


def test_create_shorts_out_if_no_commits(monkeypatch):
    monkeypatch.setattr(testee, "_has_commits_against_master", lambda: False)
    testee.create()
    mock_git_repo.push.assert_not_called()


def test_create_marks_ticket_rfr_if_requested(monkeypatch):
    testee.create(rfr=True)

    mock_workitems.update.assert_called_once_with(
        mock_workitems.get_work_item.return_value,
        {
            "status": "Ready for Review",
            "details": "PR created: "
            + mock_gh.create_pr.return_value.html_url
            + "\n\n"
            + WI_BODY,
            "details_and_steps_to_reproduce": "PR created: "
            + mock_gh.create_pr.return_value.html_url
            + "\n\n"
            + WI_BODY,
        },
    )


def test_create_adds_feed_post_if_requested(monkeypatch):
    testee.create(rfr=True)

    mock_workitems.add_feed_post.assert_called_once_with(
        mock_workitems.get_work_item.return_value,
        "PR created: " + mock_gh.create_pr.return_value.html_url,
    )


def test_create_passes_editor_return_to_create(monkeypatch):
    testee.create()

    mock_gh.create_pr.assert_called_once_with(
        repo_name=REPO_NAME,
        title="@W-1234@ " + WI_SUBJECT,
        body=EDIT_RETURN,
        head=BRANCH_NAME,
        draft=False,
    )


def test_create_passes_updated_body_to_editor(monkeypatch):
    gus_placeholder = "<!-- Link to GUS work item(s)-->"
    jenkins_placeholder = "<!-- Link to Jenkins build, if applicable-->"
    desc_placeholder = "<!-- A brief description of changes -->"
    fake_body = (
        f"gus:{gus_placeholder}\njenkins:{jenkins_placeholder}\ndesc:{desc_placeholder}"
    )

    monkeypatch.setattr(testee, "_read_body_template", lambda: fake_body)
    testee.create()

    expected = (
        "gus:https://gus.my.salesforce.com/apex/ADM_WorkLocator?bugorworknumber=W-1234\n"
        "jenkins:https://jenkins.devergage.com/job/evergage-product/job/myteam%252F@W-1234@-test\n"
        "desc:Hello World"
    )
    mock_edit.edit.assert_called_once_with(expected)


def test_create_reads_body_template_from_default_file(monkeypatch):
    monkeypatch.delattr(testee, "_read_body_template")  # use the real one
    mopen = mock_open(read_data="Bobobobob")
    monkeypatch.setattr(builtins, "open", mopen)

    testee.create()
    mopen.assert_called_once_with(".github/PULL_REQUEST_TEMPLATE.md")


def test_create_reads_body_template_from_custom_file(monkeypatch):
    monkeypatch.delattr(testee, "_read_body_template")  # use the real one
    mopen = mock_open(read_data="Bobobobob")
    monkeypatch.setattr(builtins, "open", mopen)
    monkeypatch.setattr(os.path, "exists", lambda x: True)

    mock_config._config = {"PRs": {"body_template": ".github/OTHER_TEMPLATE.md"}}
    testee.create()
    mopen.assert_called_with(".github/OTHER_TEMPLATE.md")


def test_list_works(monkeypatch):
    mock_config._config = {
        "PRs": {
            "queries": {
                "default": "repo:evergage/evergage-platform author:${username}"
            },
            "team_prefix": "myteam",
        }
    }
    mock_gh.get_username.return_value = "bobobobob"
    mock_gh.query_prs.return_value = ["pr1", "pr2"]
    actual = testee.list_prs("default")

    mock_gh.query_prs.assert_called_once_with(
        "repo:evergage/evergage-platform author:bobobobob"
    )
    assert actual == ["pr1", "pr2"]

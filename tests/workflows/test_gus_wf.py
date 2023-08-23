from unittest.mock import MagicMock, ANY

import pytest

from gitgus.config import Config
from gitgus.workflows.gus_wf import GusWorkflow
from gitgus.gus.sobjects.work import Work
from gitgus.gus.gus_client import GUSClient
from tests.testing_utils import create_wi
from tests.workflows.test_utils import _create_branch

testee: GusWorkflow
mock_config: MagicMock
mock_edit: MagicMock
mock_git_repo: MagicMock
mock_workitems: MagicMock
mock_wi: Work

EDIT_RETURN = "Descriptions"
BRANCH_NAME = "myteam/@W-1234@-test"
REPO_NAME = "myteam/awesome"
WI_SUBJECT = "Hello World"


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
    global testee, mock_config, mock_edit, mock_git_repo, mock_workitems, mock_wi
    monkeypatch.setattr(GUSClient, "_connect_gus_with_sso", MagicMock())
    monkeypatch.setattr(Work, "soql_query", MagicMock())
    mock_wi = create_wi("W-1234", WI_SUBJECT)
    Work.soql_query.return_value = [mock_wi]
    mock_config = Config()
    mock_config.load_defaults()
    mock_config.load_global_init_values()
    mock_config.set("PRs.team_prefix", "myteam")
    mock_gh = MagicMock()
    mock_gh.get_repos.return_value = []
    mock_workitems = MagicMock()
    mock_edit = MagicMock()
    mock_edit.edit.return_value = EDIT_RETURN
    mock_git_repo = MagicMock()
    mock_workitems.user_id.return_value = "mario"

    testee = GusWorkflow(
        config=mock_config,
        external_editor=mock_edit,
        git_repo=mock_git_repo,
        work_items=mock_workitems,
    )


def test_list():
    Work.soql_query.return_value = ["hello", "world"]
    mock_config.set(
        "GUS.queries.default",
        "WHERE Assignee__c = '${me}' AND (NOT Status__c  LIKE 'Closed%')",
    )
    actual = testee.query("default")
    assert actual == ["hello", "world"]
    assert Work.soql_query.call_args[0][0] == "WHERE Assignee__c = 'mario' AND (NOT Status__c  LIKE 'Closed%')"


def test_set_status():
    testee.set_status("W-1234", "In Progress")
    mock_workitems.update.assert_called_once_with(mock_wi, {"status": "In Progress"})


def test_set_status_not_found_raises():
    Work.soql_query.return_value = []
    with pytest.raises(Exception, match="Work item W-1234 not found"):
        testee.set_status("W-1234", "In Progress")
    mock_workitems.update.assert_not_called()


def test_checkout_creates_new_branch():
    Work.soql_query.return_value = [
        create_wi("W-1234", "Hello World"),
        create_wi("W-456", "Bye World"),
    ]
    mock_prompt = MagicMock()
    mock_prompt.return_value = 0
    testee.checkout(mock_prompt)
    mock_git_repo.checkout.assert_called_once_with("myteam/@W-1234@-Hello-World", create=True)


def test_checkout_checks_out_existing_branch():
    Work.soql_query.return_value = [
        create_wi("W-1234", "Hello World"),
        create_wi("W-456", "Bye World"),
    ]
    mock_prompt = MagicMock()
    mock_prompt.return_value = 0
    mock_git_repo.get_branches.return_value = [_create_branch("myteam/@W-1234@-Work-in-progress")]
    testee.checkout(mock_prompt)
    mock_git_repo.checkout.assert_called_once_with("myteam/@W-1234@-Work-in-progress")


def test_checkout_returns_none_when_no_tickets_found():
    Work.soql_query.return_value = []
    mock_prompt = MagicMock()
    mock_prompt.return_value = 0
    assert testee.checkout(mock_prompt) is None
    mock_git_repo.checkout.assert_not_called()


def test_checkout_mark_as_in_progress():
    wi = create_wi("W-1234", "Hello World")
    Work.soql_query.return_value = [wi]
    mock_prompt = MagicMock()
    mock_prompt.return_value = 0
    mock_git_repo.get_branches.return_value = [_create_branch("myteam/@W-1234@-Work-in-progress")]
    testee.checkout(mock_prompt, mark_as_in_progress=True)
    mock_git_repo.checkout.assert_called_once_with("myteam/@W-1234@-Work-in-progress")
    mock_workitems.update.assert_called_once_with(ANY, {"status": "In Progress"})


def test_get_returns_work_item():
    wi = create_wi("W-1234", "Hello World")
    Work.soql_query.return_value = [wi]
    actual = testee.get("W-1234")
    assert actual == wi
    Work.soql_query.assert_called_once_with("WHERE Name = 'W-1234'")

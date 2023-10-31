from unittest.mock import MagicMock, ANY

import pytest

from gitgus.config import Config
from gitgus.gus.sobjects.build import Build
from gitgus.gus.sobjects.work import Work
from tests.testing_utils import create_wi, create_build
from gitgus.workflows.release_wf import ReleaseWorkflow

testee: ReleaseWorkflow
mock_config: Config
mock_edit: MagicMock
mock_gh: MagicMock
mock_git_repo: MagicMock
mock_workitems: MagicMock

REPO_NAME = "myteam/awesome"


def _create_tag(name, sha):
    tag = MagicMock()
    tag.name = name
    tag.commit.sha = sha
    return tag


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
    global testee, mock_config, mock_edit, mock_gh, mock_git_repo, mock_workitems
    mock_config = Config()
    mock_config._config = {}

    mock_gh = MagicMock()
    mock_gh.compare_tags.return_value = mock_comparison([1234, 4567, 8901])
    mock_gh.get_tags.return_value = [
        _create_tag("v1.0.0", "0x1234FFFFF"),
        _create_tag("v1.0.1", "0x4567FFFFF"),
    ]
    mock_gh.query_prs.return_value = [mock_pr(1234), mock_pr(4567), mock_pr(8901)]

    mock_git_repo = MagicMock()
    mock_git_repo.get_repo_name.return_value = REPO_NAME

    monkeypatch.setattr(Work, "soql_query", MagicMock())
    Work.soql_query.side_effect = [
        [create_wi("W-1234", "Hello World")],
        [create_wi("W-4567", "Hello World")],
        [create_wi("W-8901", "Hello World")],
    ]

    monkeypatch.setattr(Work, "update", MagicMock())

    monkeypatch.setattr(Build, "soql_query", MagicMock())
    Build.soql_query.return_value = [create_build()]

    mock_workitems = MagicMock()
    mock_workitems.add_feed_post.return_value = MagicMock()

    testee = ReleaseWorkflow(
        mock_config, mock_gh, mock_git_repo, mock_workitems, MagicMock()
    )


def mock_pr(num: int):
    pr = MagicMock()
    pr.title = f"W-{num}: Hello World"
    pr.number = 1234
    pr.body = "Hello World"
    pr.merge_commit_sha = f"0x{num}FFFFFFFF"
    pr.head.label = f"myteam/w-{num}-hello-world"
    return pr


def mock_comparison(nums: list[int]):
    comparison = MagicMock()
    comparison.commits = [
        MagicMock(),
        MagicMock(),
        MagicMock(),
    ]
    for n, num in enumerate(nums):
        comparison.commits[n].message = f"W-{num}: Hello World"
        comparison.commits[n].sha = f"0x{num}FFFFFFFF"

    return comparison


def test_list_released_does_not_catch_fire():
    actual = testee.list_released("v1.0.0", "v1.0.1")
    assert len(actual) == 3
    wi, pr = actual[0]
    assert Work.soql_query.call_count == 3
    assert pr.title == "W-1234: Hello World"
    assert wi.subject == "Hello World"
    mock_gh.get_tags.assert_called_once_with(REPO_NAME)
    mock_gh.compare_tags.assert_called_once_with(REPO_NAME, ANY, ANY)


def test_list_released_when_pr_has_no_ticket():
    Work.soql_query.side_effect = [
        [create_wi("W-1234", "Hello World")],
        [],
        [create_wi("W-8901", "Hello World")],
    ]

    actual = testee.list_released("v1.0.0", "v1.0.1")

    assert len(actual) == 3
    wi, pr = actual[0]
    assert pr.title == "W-1234: Hello World"
    assert wi.subject == "Hello World"
    wi, pr = actual[1]
    assert pr.title == "W-4567: Hello World"
    assert wi is None
    wi, pr = actual[2]
    assert pr.title == "W-8901: Hello World"
    assert wi.subject == "Hello World"


def test_update_tickets_when_pr_ticket_not_in_title():
    pr1 = mock_pr(1234)
    pr1.title = "Hello World"

    mock_gh.query_prs.return_value = [pr1, mock_pr(4567), mock_pr(8901)]

    wi1 = create_wi("W-1234", "Hello World")
    Work.soql_query.side_effect = [[wi1], [wi1], [wi1]]

    stats, results = testee.update_tickets("TEST_1.0.1", "v1.0.0", "v1.0.1")

    assert stats["no_work_item"] == 0
    assert Work.soql_query.call_count == 3
    assert Work.soql_query.call_args_list[0][0][0] == "WHERE Name = 'W-1234'"
    assert Work.soql_query.call_args_list[1][0][0] == "WHERE Name = 'W-4567'"
    assert Work.soql_query.call_args_list[2][0][0] == "WHERE Name = 'W-8901'"


def test_update_tickets():
    wi1 = create_wi("W-1234", "Hello World")
    wi3 = create_wi("W-8901", "Hello World")

    Work.soql_query.side_effect = [
        [wi1],
        [],
        [wi3],
    ]

    stats, results = testee.update_tickets("TEST_1.0.1", "v1.0.0", "v1.0.1")

    assert stats["already_has_build"] == 0
    assert stats["no_work_item"] == 1
    assert stats["non_closed"] == 2
    assert stats["total"] == 3
    assert wi1.scheduled_build == "test_build_id_"
    assert wi3.scheduled_build == "test_build_id_"
    mock_gh.add_comment.assert_called_once()
    assert Work.update.call_count == 2

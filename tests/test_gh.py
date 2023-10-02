from unittest.mock import MagicMock
from github import Issue, Repository
import gitgus.gh as gh


def test_get_repos(monkeypatch):
    mock_github = MagicMock()
    monkeypatch.setattr(gh, "Github", mock_github)
    mock_github.return_value = mock_github
    mock_github.get_user.return_value = mock_github
    mock_github.get_repos.return_value = [
        Repository.Repository(MagicMock(), MagicMock(), MagicMock(), MagicMock()),
        Repository.Repository(MagicMock(), MagicMock(), MagicMock(), MagicMock()),
    ]
    testee = gh.GH("token")
    repos = testee.get_repos()
    assert len(repos) == 2


def test_get_repo(monkeypatch):
    mock_github = MagicMock()
    monkeypatch.setattr(gh, "Github", mock_github)
    mock_github.return_value = mock_github
    mock_github.get_user.return_value = mock_github
    mock_github.get_repo.return_value = Repository.Repository(
        MagicMock(), MagicMock(), MagicMock(), MagicMock()
    )
    testee = gh.GH("token")
    repo = testee.get_repo("repo")
    assert repo is not None


def test_query_prs(monkeypatch):
    mock_github = MagicMock()
    monkeypatch.setattr(gh, "Github", mock_github)
    mock_github.return_value = mock_github
    mock_issue = MagicMock()
    mock_github.search_issues.return_value = [
        mock_issue,
        mock_issue,
    ]
    testee = gh.GH("token")
    prs = testee.query_prs("query")
    assert len(prs) == 2
    mock_issue.as_pull_request.assert_called()


def test_create_pr(monkeypatch):
    mock_github = MagicMock()
    monkeypatch.setattr(gh, "Github", mock_github)
    mock_github.return_value = mock_github
    mock_github.get_user.return_value = mock_github
    mock_github.get_repo.return_value = Repository.Repository(
        MagicMock(), MagicMock(), MagicMock(), MagicMock()
    )
    monkeypatch.setattr(Repository.Repository, "create_pull", MagicMock())
    testee = gh.GH("token")
    pr = testee.create_pr("repo", "title", "body", "head")
    assert pr is not None
    Repository.Repository.create_pull.assert_called_once_with(
        title="title", body="body", head="head", base="master", draft=False
    )

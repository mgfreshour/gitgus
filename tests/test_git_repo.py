from unittest.mock import MagicMock
import gitgus.git_repo as git_repo


def test_get_branch_name(monkeypatch):
    mock_repo = MagicMock()
    mock_repo.active_branch.name = "myteam/@W-1234@-test"
    monkeypatch.setattr(git_repo, "Repo", lambda: mock_repo)
    testee = git_repo.GitRepo()

    assert testee.get_branch_name() == "myteam/@W-1234@-test"

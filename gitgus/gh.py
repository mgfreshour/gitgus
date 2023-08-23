from github import Github, PullRequest, Repository
from github.Commit import Commit
from github.Comparison import Comparison
from github.Tag import Tag


class GH:
    def __init__(self, token: str):
        self.token = token
        self._gh = None

    @property
    def gh(self):
        if not self._gh:
            if not self.token:
                raise PermissionError("No github token provided.")
            self._gh = Github(self.token)
        return self._gh

    def get_tags(self, repo_name: str) -> list[Tag]:
        repo = self.gh.get_repo(repo_name)
        return list(repo.get_tags())

    def compare_tags(self, repo_name: str, start_tag: Tag, end_tag: Tag) -> Comparison:
        repo = self.gh.get_repo(repo_name)
        return repo.compare(start_tag.commit.sha, end_tag.commit.sha)

    def get_commit(self, repo_name: str, commit_sha: str) -> Commit:
        repo = self.gh.get_repo(repo_name)
        return repo.get_commit(commit_sha)

    def get_repos(self) -> list[Repository]:
        return list(self.gh.get_user().get_repos())

    def get_repo(self, repo_name: str) -> Repository:
        return self.gh.get_repo(repo_name)

    def get_reviews(self, pr: PullRequest):
        return list(pr.get_reviews())

    def query_prs(self, query: str) -> list[PullRequest]:
        if "is:pr" not in query:
            query += " is:pr"
        prs = list(self.gh.search_issues(query))
        return [pr.as_pull_request() for pr in prs]

    def create_pr(self, repo_name: str, title: str, body: str, head: str, draft: bool = False) -> PullRequest:
        repo = self.gh.get_repo(repo_name)
        pr = repo.create_pull(title=title, body=body, head=head, base="master", draft=draft)
        return pr

    def get_username(self):
        return self.gh.get_user().login

    def add_comment(self, pr: PullRequest, message: str):
        pr.create_issue_comment(message)

    def get_pr(self, repo_name, number):
        repo = self.gh.get_repo(repo_name)
        return repo.get_pull(number)

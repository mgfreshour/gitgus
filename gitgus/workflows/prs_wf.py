import os
import re
from datetime import datetime, timedelta

from string import Template
from github.PullRequest import PullRequest
from gitgus.gus.sobjects.work import Work

from gitgus.gus.workitems import WorkItems

from gitgus.gh import GH
from gitgus.git_repo import GitRepo
from gitgus.utils.external_editor import ExternalEditor
from gitgus.config import Config
from gitgus.jenki import Jenki


class PrWorkflow:
    def __init__(
        self,
        config: Config,
        gh: GH,
        git_repo: GitRepo,
        work_items: WorkItems,
        external_editor: ExternalEditor,
        jenki: Jenki,
    ):
        self.config = config
        self.gh = gh
        self.git_repo = git_repo
        self.work_items = work_items
        self.external_editor = external_editor
        self.jenki = jenki

    def pr_stats(self, start_date: datetime = None, end_date: datetime = None):
        """Get stats on when a PR was opened, when it received the first comment, and when it was approved"""
        if not start_date:
            start_date = datetime.now() - timedelta(days=90)
        if not end_date:
            end_date = datetime.now()

        team_prefix = self.config.get("PRs.team_prefix")

        repo_name = self.git_repo.get_repo_name()

        created_prs = self.gh.query_prs(
            f" repo:{repo_name} created:{start_date.strftime('%Y-%m-%d')}..{end_date.strftime('%Y-%m-%d')} is:pr draft:false head:{team_prefix}"
        )
        updated_prs = self.gh.query_prs(
            f" repo:{repo_name} merged:{start_date.strftime('%Y-%m-%d')}..{end_date.strftime('%Y-%m-%d')} is:pr draft:false head:{team_prefix}"
        )
        uniq_prs = {}
        for pr in created_prs:
            uniq_prs[pr.number] = pr
        for pr in updated_prs:
            uniq_prs[pr.number] = pr

        out = []
        for pr in uniq_prs.values():
            created = pr.created_at
            days_till_first_comment = None
            days_till_merge = None
            days_till_approved = None
            if pr.merged_at:
                days_till_merge = pr.merged_at - created

            events = pr.get_issue_events()
            days_till_first_review_requested = None
            times_approval_dismissed = 0
            for event in events:
                if event.event == "review_dismissed":
                    times_approval_dismissed += 1
                if (
                    event.event == "review_requested"
                    and days_till_first_review_requested is None
                ):
                    days_till_first_review_requested = event.created_at - created

            reviewers = []
            approvers = []
            reviews = pr.get_reviews()
            for review in reviews:
                if review.user.login == pr.user.login:
                    continue
                if review.user.login not in reviewers:
                    reviewers.append(review.user.login)
                if days_till_first_comment is None:
                    days_till_first_comment = review.submitted_at - created
                elif review.submitted_at - created < days_till_first_comment:
                    days_till_first_comment = review.submitted_at - created
                if review.state == "APPROVED":
                    if review.user.login not in approvers:
                        approvers.append(review.user.login)
                    if days_till_approved is None:
                        days_till_approved = review.submitted_at - created
                    elif review.submitted_at - created < days_till_approved:
                        days_till_approved = review.submitted_at - created

            pr_stat = {
                "title": pr.title,
                "user": pr.user.login,
                "additions": pr.additions,
                "deletions": pr.deletions,
                "changed_files": pr.changed_files,
                "created_at": pr.created_at,
                "updated_at": pr.updated_at,
                "days_till_first_review_requested": days_till_first_review_requested,
                "days_till_first_comment": days_till_first_comment,
                "days_till_approved": days_till_approved,
                "days_till_merged": days_till_merge,
                "times_approval_dismissed": times_approval_dismissed,
                "merged_by": pr.merged_by.login if pr.merged_by else None,
                "requested_reviewers": ", ".join(
                    [rr.login for rr in pr.requested_reviewers]
                ),
                "actual_reviewers": ", ".join(reviewers),
                "approvers": ", ".join(approvers),
            }
            out.append(pr_stat)
        return out

    def create(
        self, draft: bool = False, rfr: bool = False, assign: bool = False
    ) -> [PullRequest, Work]:
        """Create a PR."""
        self.git_repo.push()
        if not self._has_commits_against_master():
            return None, None
        branch_name = self.git_repo.get_branch_name()
        repo = self.git_repo.get_repo_name()
        wi_id = self._extract_wi_id(branch_name)
        wi = Work.get_by_name(wi_id)
        body = self._get_body(wi_id, branch_name, wi.subject)

        subject = f"@{wi_id}@ {wi.subject}"
        pr = self.gh.create_pr(
            repo_name=repo, title=subject, body=body, head=branch_name, draft=draft
        )
        if rfr:
            if wi.details_and_steps_to_reproduce:
                body = wi.details_and_steps_to_reproduce
                if wi.details:
                    body += "\n\n" + wi.details
            else:
                body = wi.details
            body = "PR created: " + pr.html_url + "\n\n" + body
            self.work_items.update(
                wi,
                {
                    "status": "Ready for Review",
                    "details": body,
                    "details_and_steps_to_reproduce": body,
                },
            )
            self.work_items.add_feed_post(wi, "PR created: " + pr.html_url)

        if assign:
            reviewers = self.config.get("PRs.reviewers")
            pr.create_review_request(reviewers)
            # reload the PR so assigned will show up
            pr = self.gh.get_pr(repo, pr.number)

        return pr, wi

    def _extract_wi_id(self, branch_name):
        match = re.search(r"(W-\d+)", branch_name)
        if not match:
            raise Exception(
                f"Branch name {branch_name} is not in the correct format. Expected team/@W-1234@-description"
            )
        wi_id = match.group(1)
        return wi_id

    def _get_body(self, wi_id, branch_name, description):
        """Get the body of the PR."""
        gus_placeholder = "<!-- Link to GUS work item(s)-->"
        jenkins_placeholder = "<!-- Link to Jenkins build, if applicable-->"
        desc_placeholder = "<!-- A brief description of changes -->"

        body = self._read_body_template()

        body = body.replace(
            gus_placeholder,
            "https://gus.my.salesforce.com/apex/ADM_WorkLocator?bugorworknumber="
            + wi_id,
        )
        body = body.replace(
            jenkins_placeholder,
            "https://jenkins.devergage.com/job/evergage-product/job/"
            + branch_name.replace("/", "%252F"),
        )
        body = body.replace(desc_placeholder, description)

        body = self.external_editor.edit(body)

        return body

    def _read_body_template(self):
        if not self.config.get("PRs.body_template") or not os.path.exists(
            self.config.get("PRs.body_template")
        ):
            return ""
        with open(self.config.get("PRs.body_template")) as f:
            body = f.read()
        return body

    def list_prs(self, query_name: str) -> list[PullRequest]:
        """List PRs."""
        username = self.gh.get_username()
        repo_name = self.git_repo.get_repo_name()
        team_prefix = self.config.get("PRs.team_prefix")
        query = Template(self.config.get(f"PRs.queries.{query_name}")).safe_substitute(
            username=username, repo=repo_name, team_prefix=team_prefix
        )
        prs = self.gh.query_prs(query)
        return prs

    def list_pr_builds(self, query_name: str) -> list:
        """List PRs."""
        repo_name = self.git_repo.get_repo_name()
        job_name = repo_name.split("/")[-1]

        prs = self.list_prs(query_name)
        builds = []
        for pr in prs:
            branch_name = pr.head.ref.replace("/", "%252F")
            job = self.jenki.get_branch_job(job_name, branch_name)
            last_build = (
                job["lastCompletedBuild"]["number"] if job["lastCompletedBuild"] else 0
            )
            last_success = (
                job["lastSuccessfulBuild"]["number"]
                if job["lastSuccessfulBuild"]
                else 0
            )
            last_unstable = (
                job["lastUnstableBuild"]["number"] if job["lastUnstableBuild"] else 0
            )
            last_failure = (
                job["lastUnsuccessfulBuild"]["number"]
                if job["lastUnsuccessfulBuild"]
                else 0
            )
            if last_build == 0:
                status = "NO BUILDS"
            elif last_build == last_unstable:
                status = "UNSTABLE"
            elif last_build == last_success:
                status = "SUCCESS"
            elif last_build == last_failure:
                status = "FAILURE"
            else:
                status = "UNKNOWN"

            test_report = self.jenki.get_build_test_report(
                f"{job_name}/{branch_name}", last_build
            )
            failed_tests = []
            if test_report and test_report["failCount"] > 0:
                for suite in test_report["suites"]:
                    for case in suite["cases"]:
                        if case["status"] not in ["PASSED", "SKIPPED", "FIXED"]:
                            failed_tests.append(case["className"] + ":" + case["name"])

            builds.append(
                {
                    "title": pr.title,
                    "pr": pr.html_url,
                    "status": status,
                    "build_url": job["url"],
                    "failed_tests": failed_tests,
                }
            )
        return builds

    def attach_reviewers(self, chooser) -> list[PullRequest]:
        prs = self.list_prs("mine")
        choices = [f"{pr.title} ({len(pr.requested_reviewers)})" for pr in prs]
        n = chooser(choices)
        pr = prs[n]

        reviewers = self.config.get("PRs.reviewers")
        pr.create_review_request(reviewers)

        # reload the PR
        repo_name = self.git_repo.get_repo_name()
        pr = self.gh.get_pr(repo_name, pr.number)

        return [pr]

    def _has_commits_against_master(self):
        """Check if there are any commits against master."""
        branch_name = self.git_repo.get_branch_name()
        repo_name = self.git_repo.get_repo_name()
        repo = self.gh.get_repo(repo_name)
        default_branch = repo.default_branch
        commits = repo.compare(default_branch, branch_name).commits
        return len(commits) > 0

import re

from click import UsageError
from github.PullRequest import PullRequest
from simple_salesforce import SalesforceResourceNotFound

from gitgus.gus.sobjects.work import Work

from gitgus.config import Config
from gitgus.gh import GH
from gitgus.git_repo import GitRepo
from gitgus.gus.workitems import WorkItems, RECORD_TYPES
from gitgus.gus.builds import Builds
from gitgus.gus.sobjects.build import Build

MAX_QUERY_LENGTH = 256
HASH_LENGTH = 7


class ReleaseWorkflow:
    def __init__(self, config: Config, gh: GH, git_repo: GitRepo, work_items: WorkItems, builds: Builds):
        self.config = config
        self.gh = gh
        self.git_repo = git_repo
        self.work_items = work_items
        self.builds = builds
        self.dry_run = False

    def update_tickets(self, gus_build: str, start_tag_name: str, end_tag_name: str):
        """Update the tickets in GUS."""
        repo_name = self.git_repo.get_repo_name()
        if not repo_name:
            raise UsageError("Could not find git repo in CWD")
        build = Build.get_by_name(gus_build)
        if not build:
            raise UsageError(f"Could not find build {gus_build}")
        commits = self._get_commits_between_tags(repo_name, start_tag_name, end_tag_name)
        if not commits:
            raise UsageError(f"No commits found between {start_tag_name} and {end_tag_name}")
        prs = self._get_prs_with_merge_commits(repo_name, commits)
        if not prs:
            raise UsageError(f"No PRs found for commits between {start_tag_name} and {end_tag_name}")

        stats = {
            "total": len(prs),
            "updated_build": 0,
            "no_work_item": 0,
            "non_closed": 0,
            "already_has_build": 0,
            "total_bugs": 0,
            "total_user_stories": 0,
        }
        results = []
        for pr in prs:
            work_item = self._get_gus_work_item(pr.title + " " + pr.head.label)
            results.append([work_item, pr])
            if work_item:
                stats["total_bugs"] += 1 if work_item.record_type_id == RECORD_TYPES["Bug"] else 0
                stats["total_user_stories"] += 1 if work_item.record_type_id == RECORD_TYPES["User Story"] else 0
                if work_item.scheduled_build is not None:
                    stats["already_has_build"] += 1

                self._update_ticket_build(work_item, build)
                stats["updated_build"] += 1

                if work_item.status != "Closed":
                    self._comment_on_wi(
                        work_item,
                        f"AUTOMATED MSG: PR {pr.html_url} was released in {build.name}."
                        + " Please update ticket status.",
                    )
                    stats["non_closed"] += 1
            else:
                self._comment_on_pr(
                    pr,
                    "AUTOMATED MSG: PR Released. Could not find a GUS work item in the PR title. "
                    + f"Please update your work item with the build {build.name}.\n"
                    + "Did you know you can use the `gitgus` tool to create a branch and PR for a GUS work item?",
                )
                stats["no_work_item"] += 1

        return stats, results

    def _update_ticket_build(self, work_item, build):
        if work_item.scheduled_build == build.id_:
            print(f"Skipping update of {work_item.name}, build already set to {build.name}")
        if self.dry_run:
            print(f"Updating {work_item.name} with build to {build.name}")
        else:
            work_item.scheduled_build = build.id_
            try:
                Work.update(work_item)
            except Exception as e:
                print(f"Error updating {work_item.name} with build to {build.name}: {e}")

    def list_released(self, start_tag_name: str, end_tag_name: str):
        """List the released PRs."""
        repo_name = self.git_repo.get_repo_name()
        commits = self._get_commits_between_tags(repo_name, start_tag_name, end_tag_name)

        prs = self._get_prs_with_merge_commits(repo_name, commits)
        results = []
        for pr in prs:
            work_item = self._get_gus_work_item(pr.title + " " + pr.head.label)
            results.append([work_item, pr])
        return results

    def _get_prs_with_merge_commits(self, repo_name, commit_hashes):
        base_query = f" repo:{repo_name} is:pr is:merged"
        batch_size = (MAX_QUERY_LENGTH - len(base_query)) // (HASH_LENGTH + 1)
        hash_prefixes = [c[:HASH_LENGTH] for c in commit_hashes]

        batches = []
        while hash_prefixes:
            batch, hash_prefixes = (
                hash_prefixes[:batch_size],
                hash_prefixes[batch_size:],
            )
            batches.append(batch)

        prs = []
        for batch in batches:
            batch_prs = self.gh.query_prs(" ".join(batch) + base_query)
            prs.extend(batch_prs)
        released_prs = []
        for pr in prs:
            if pr.merge_commit_sha in commit_hashes:
                released_prs.append(pr)

        return released_prs

    def _get_commits_between_tags(self, repo_name, start_tag_name, end_tag_name):
        tags = self.gh.get_tags(repo_name)
        start_tag = None
        end_tag = None
        for tag in tags:
            if tag.name == start_tag_name:
                start_tag = tag
            if tag.name == end_tag_name:
                end_tag = tag
            if start_tag and end_tag:
                break
        if not start_tag or not end_tag:
            raise UsageError(f"Could not find tags {start_tag_name} and {end_tag_name}")
        cmp = self.gh.compare_tags(repo_name, start_tag, end_tag)
        commit_hashes = []
        for commit in cmp.commits:
            commit_hashes.append(commit.sha)
        return commit_hashes

    def _get_gus_work_item(self, title):
        match = re.search(r"[wW][ -](\d+)", title)
        if match:
            work_item_id = "W-" + match.group(1)
            try:
                return Work.get_by_name(work_item_id)
            except SalesforceResourceNotFound as e:
                print(f"Could not find a GUS work item in the PR title: '{work_item_id}' - ${e}")
                return None
        else:
            print(f"Could not find a GUS work item in the PR title: {title}")
            return None

    def _comment_on_pr(self, pr: PullRequest, message: str):
        if self.dry_run:
            print(f"Commenting on PR {pr.html_url}: {message}")
        else:
            self.gh.add_comment(pr, message)

    def _comment_on_wi(self, work_item: Work, message: str):
        if self.dry_run:
            print(f"Commenting on WI {work_item.name}: {message}")
        else:
            self.work_items.add_feed_post(work_item, message)

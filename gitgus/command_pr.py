from csv import writer

import typer
from github import Consts
from rich import print

from gitgus.utils.console_writer import print_work_item
from gitgus.workflows.prs_wf import PrWorkflow
from gitgus.deps import config, gh, git_repo, work_items, external_editor, jenki
from gitgus.utils.slack_writer import SlackWriter
from gitgus.utils.console_writer import print_prs
from gitgus.utils.menu import get_choice

pr_app = typer.Typer(no_args_is_help=True)

prs = PrWorkflow(config, gh, git_repo, work_items, external_editor, jenki)


@pr_app.command()
def pr_stats():
    stats = prs.pr_stats()
    with open("/Users/mfreshour/Desktop/pr-stats.csv", "w") as f:
        w = writer(f)
        headers = [f.replace("_", " ").title() for f in stats[0].keys()]
        w.writerow(headers)

        for pr_stat in stats:
            w.writerow(pr_stat.values())


@pr_app.command()
def my_pr_builds():
    """List PR and their most recent build status."""
    builds = prs.list_pr_builds("mine")
    for build in builds:
        if build["status"] == "SUCCESS":
            color = "green"
        elif build["status"] == "UNSTABLE":
            color = "yellow"
        else:
            color = "red"

        print(build["title"])
        print(
            f"    [{color}]{build['pr']} | {build['status']} | {build['build_url']}[/]"
        )
        if build["failed_tests"]:
            print(f"    Failed tests: {len(build['failed_tests'])}")
            for failed_test in build["failed_tests"][0:5]:
                print(f"    - {failed_test}")
        print()


@pr_app.command()
def create(
    draft: bool = typer.Option(False, "--draft", "-d", help="Create a draft PR"),
    rfr: bool = typer.Option(
        True,
        "--rfr/--no-rfr",
        "-r/-R",
        help="Create a PR and mark ticket as ready for review",
    ),
    assign: bool = typer.Option(
        False, "--assign/--no-assign", "-a/-A", help="Assign reviewers to PR"
    ),
):
    """Create a PR."""
    pr, wi = prs.create(draft=draft, rfr=rfr, assign=assign)
    if not pr:
        print("No PR created. Are there commits to push?")
        return
    print(f"Created PR {pr.html_url}")
    if rfr:
        print("Ticket marked as ready for review: ")
        print_work_item(wi)


@pr_app.command(name="list")
def list_prs():
    """List PRs."""
    print_prs(prs.list_prs("default"))


@pr_app.command()
def query(
    query_name: str = typer.Argument(..., help="The name of the query to run"),
    slack_chan: str = typer.Option(
        None, "--slack", "-s", help="Slack channel to post to"
    ),
):
    """Use configured query for PRs."""
    pr_list = prs.list_prs(query_name)
    if slack_chan:
        slack_writer = SlackWriter(config)
        # slack_writer.post_prs(pr_list, slack_chan)
        print(slack_writer.format_prs(pr_list))
    else:
        print_prs(pr_list)


@pr_app.command()
def mine():
    """Use configured query for PRs."""
    print_prs(prs.list_prs("mine"))


@pr_app.command()
def add_reviewers():
    """Add reviewers to all tickets."""
    res = prs.attach_reviewers(get_choice)
    print_prs(res)

import os

import typer

from rich import print

from gitgus.deps import config, work_items, external_editor, git_repo
from gitgus.workflows.gus_wf import GusWorkflow
from gitgus.utils.menu import get_choice
from gitgus.utils.console_writer import print_work_item, print_wi_table, print_wi_csv
from gitgus.utils.console_input import choose_gus_team

gus_app = typer.Typer(no_args_is_help=True)

gus_wf = GusWorkflow(config, work_items, external_editor, git_repo)


@gus_app.command()
def sort_tickets(
    team_name: str = typer.Option(
        "", help="The name of the team to report on (can be partial)"
    ),
    release_name: str = typer.Option(
        "", help="The name of the release to report on (can be partial)"
    ),
    dry_run: bool = typer.Option(
        False, help="Don't actually update the tickets, just print what would happen"
    ),
    file_name: str = typer.Option(
        os.path.expanduser("~") + "/Desktop/tickets.csv",
        help="The name of the file to write to",
    ),
):
    if team_name == "":
        team_name = typer.prompt("What team do you want to report on? (can be partial)")
        # team_name = choose_gus_team().name
    if release_name == "":
        release_name = typer.prompt(
            "What release do you want to report on? (can be partial)"
        )
    tickets = gus_wf.sort_tickets(team_name, release_name, dry_run)
    for ticket in tickets:
        ticket["url"] = (
            "https://gus.my.salesforce.com/apex/ADM_WorkLocator?bugorworknumber="
            + ticket["name"]
        )
    print(f"Writing {len(tickets)} tickets to {file_name}")
    print_wi_csv(
        file_name,
        tickets,
        [
            "work_id_and_subject",
            "status",
            "priority",
            "epic",
            "priority_rank",
            "old_rank",
            "url",
        ],
    )


# @gus_app.command()
# def test_report(
#     release_name: str = typer.Option("", prompt=True, help="The name of the release to report on (can be partial)")
#     team_name: str = typer.Option("", prompt=True, help="The name of the team to report on (can be partial)")
# ):
#     team = Team.get_by_name_like(team_name)
#     release = Release.get_by_name_li(release_name, team)
#
#     res = gus_wf.work_items.get_epics(team, release)
#
#     res.sort(key=lambda x: x[0].priority or 0, reverse=False)
#     for epic, wis in res:
#         match epic.health:
#             case "On Track":
#                 icon = "🛣️"
#             case "Completed":
#                 icon = "🏁"
#             case _:
#                 icon = "🚦"
#         print(f"{icon} {epic.priority} {epic.name} ({epic.health})")
#         gus_wf.work_items.hydrate_work_items(wis)
#         wis.sort(key=lambda x: x.status)
#         closed_count = 0
#         not_started_count = 0
#         for wi in wis:
#             if wi.status in ("Closed", "Pending Release"):
#                 closed_count += 1
#                 continue
#             elif wi.status in ("Never", "Duplicate"):
#                 continue
#             elif wi.status in ("New", "Triaged"):
#                 not_started_count += 1
#                 continue
#             icon = "🏎️" if wi.status in ("In Progress", "Ready for Review") else "❓"
#             url = wi.web_url
#             title = wi.work_id_and_subject[0:50]
#             print(f"   {icon} [{title}]({url}) - {wi.assignee} ({wi.status})")
#         print(f"   ✅ {closed_count} closed tickets")
#         print(f"   🎁 {not_started_count} not started tickets")


@gus_app.command(name="list")
def list_work(
    query_name: str = typer.Argument(
        default="default", help="The name of the query to run"
    )
):
    """Use configured query for PRs."""
    res = gus_wf.query(query_name)
    print_wi_table(res)


@gus_app.command()
def checkout(
    mark_ip: bool = typer.Option(
        True, "--ip/--no-ip", "-m/-M", help="Mark ticket as in progress"
    )
):
    """Checkout a branch for a ticket."""
    _checkout(mark_ip)


def _checkout(mark_ip):
    br, wi = gus_wf.checkout(get_choice, mark_ip)
    print(f"Checked out {br}")
    if mark_ip:
        print("Ticket marked as in progress")
        print_work_item(wi)


@gus_app.command()
def get(work_id: str):
    """Get a ticket."""
    wi = gus_wf.get(work_id)
    print_work_item(wi)


@gus_app.command()
def close(
    work_id: str,
    never: bool = typer.Option(False, "--never", "-n"),
    dekanban: bool = typer.Option(False, "--dekanban", "-d"),
):
    """Close a ticket."""
    wi = gus_wf.set_status(
        work_id,
        "Never" if never else "Closed",
    )
    if dekanban:
        gus_wf.dekanban(work_id)
    print_work_item(wi)


@gus_app.command()
def dekanban(work_id: str):
    """Remove a ticket from the kanban board."""
    wi = gus_wf.dekanban(work_id)
    print("Ticket removed from kanban board")
    print_work_item(wi)


@gus_app.command()
def swap_details(work_id: str):
    """Swap the details and details_and_steps_to_reproduce of a ticket."""
    wi = gus_wf.swap_bug_story_details(work_id)
    print("Details and subject swapped")
    print_work_item(wi)

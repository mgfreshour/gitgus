import typer

from rich import print
from rich.table import Table

from gitgus.deps import config, gh, git_repo, work_items, builds
from gitgus.workflows.release_wf import ReleaseWorkflow

release_wf = ReleaseWorkflow(config, gh, git_repo, work_items, builds)
release_app = typer.Typer(no_args_is_help=True)


@release_app.command(name="update-tickets")
def update_tickets(
    gus_build: str = typer.Option(..., prompt=True, help="GUS build, ex: MCIS_240.12"),
    start_tag: str = typer.Option(..., prompt=True, help="Previous Release tag, ex: v242.1"),
    end_tag: str = typer.Option(..., prompt=True, help="Fresh Release tag, ex: v242.2"),
    dry_run: bool = typer.Option(False, help="Do not actually update tickets and PRs, only print"),
):
    """Update the tickets in GUS."""
    release_wf.dry_run = dry_run
    stats, results = release_wf.update_tickets(gus_build, start_tag, end_tag)
    _print_results(results)
    print(f"Total PRs: {stats['total']}")
    print(f"Updated build: {stats['updated_build']}")
    print(f"Total User Stories: {stats['total_user_stories']}")
    print(f"Total Bugs: {stats['total_bugs']}")
    print(f"No work item: {stats['no_work_item']}")
    print(f"Non-closed: {stats['non_closed']}")
    print(f"Already has build: {stats['already_has_build']}")


@release_app.command(name="list")
def list_released(
    start_tag: str = typer.Argument(..., help="Release tag, ex: v242.1"),
    end_tag: str = typer.Argument(..., help="Release tag, ex: v242.2"),
):
    """List the released PRs."""
    results = release_wf.list_released(start_tag, end_tag)
    _print_results(results)


def _print_results(results):
    table = Table(header_style=config.get("GUS.style.table_header"))
    table.add_column("PR")
    table.add_column("PR URL", width=54)
    table.add_column("WI")
    table.add_column("assigned to")
    table.add_column("status")
    table.add_column("WI URL", width=54)
    for result in results:
        work_item, pr = result
        if work_item:
            table.add_row(
                pr.title,
                pr.html_url,
                work_item.work_id_and_subject,
                work_item.assignee_name,
                work_item.status,
                work_item.web_url,
            )
        else:
            table.add_row(pr.title, pr.html_url, "", "", "", "")
    print(table)

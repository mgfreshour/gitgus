from datetime import datetime, timedelta, date

import typer
from rich import print

from gitgus.utils.console_writer import print_work_item

from gitgus.workflows.flaky_wf import FlakyWorkflow, TICKET_TYPE_FIX, TICKET_TYPE_DISABLE
from gitgus.deps import config, work_items, jenki, git_repo

flaky_app = typer.Typer(no_args_is_help=True)

flaky = FlakyWorkflow(config, work_items, jenki, git_repo)


@flaky_app.command(help="Find all the builds with a flaky test in them")
def report_all_builds(
    job_name_like: str = typer.Argument("evergage-product", help="Partial name of the jobs to report on"),
    start_date: datetime = typer.Option(default=datetime.now() - timedelta(days=60), help="Start date"),
    end_date: datetime = typer.Option(default=datetime.now(), help="End date"),
):
    # date range to be inclusive
    end_date = datetime(end_date.year, end_date.month, end_date.day) + timedelta(days=1) - timedelta(seconds=1)
    start_date = datetime(start_date.year, start_date.month, start_date.day)

    all_results_count, job_result_count = flaky.build_report(job_name_like, start_date, end_date)

    print(f"Results between {start_date} and {end_date}")
    total = sum(all_results_count.values())
    print(f"Total builds: {total}")
    for k, v in all_results_count.items():
        print(f"{k}: {v} %{round(v/total*100, 2)}")

    for job, counts in job_result_count.items():
        print(f"\n{job}")
        total = sum(counts.values())
        for k, v in counts.items():
            print(f"{k}: {v} %{round(v/total*100, 2)}")


@flaky_app.command()
def report_failed_builds(
    job_name_like: str = typer.Argument("evergage-product", help="Partial name of the jobs to report on"),
    start_date: datetime = typer.Option(default=datetime.now() - timedelta(days=60), help="Start date"),
    end_date: datetime = typer.Option(default=datetime.now(), help="End date"),
):
    # date range to be inclusive
    end_date = datetime(end_date.year, end_date.month, end_date.day) + timedelta(days=1) - timedelta(seconds=1)
    start_date = datetime(start_date.year, start_date.month, start_date.day)

    function_tickets = flaky.get_flaky_tagged_tests()

    all_testcases, total_builds = flaky.report(job_name_like, start_date, end_date)
    per_count = {}
    oldest_build = datetime.now()

    for case in all_testcases:
        ts = datetime.strptime(case["timestamp"], "%d %b %Y %H:%M:%S %Z")  # '19 May 2023 15:56:36 GMT'
        if ts < oldest_build:
            oldest_build = ts
        name = case["className"] + ":" + case["name"]
        per_count[name] = per_count.get(name, 0) + 1
    results = {k: v for k, v in sorted(per_count.items(), key=lambda item: item[1], reverse=True)}
    print(f"Total builds: {total_builds}")
    print(f"Oldest build: {oldest_build}")
    for k, v in results.items():
        tickets = ["No Tickets Found"]
        if k in function_tickets:
            tickets = function_tickets[k]
        print(f"{v},{k},{'; '.join(tickets)}")


@flaky_app.command()
def create_tickets(
    build: str = typer.Option(default=0, help="Build number test failed in", prompt=True),
    job_name: str = typer.Option(default="", help="Name of the job"),
    no_fix_ticket: bool = typer.Option(default=False, help="Don't create a fix ticket"),
    no_disable_ticket: bool = typer.Option(default=False, help="Don't create a disable ticket"),
):
    """Creates the tickets for a flaky test."""
    build = int(build)
    ticket_types = []
    if not no_fix_ticket:
        ticket_types.append(TICKET_TYPE_FIX)
    if not no_disable_ticket:
        ticket_types.append(TICKET_TYPE_DISABLE)
    wis = flaky.create(build, job_name, "master", ticket_types)
    if len(wis) == 0:
        print("No tickets created")
        return
    print("Created ticket to disable:")
    print_work_item(wis[0])
    if len(wis) == 1:
        return
    print("Created ticket to fix:")
    print_work_item(wis[1])
    print("Remember to update the product tag and add the stack trace to the fix ticket!")

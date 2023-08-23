import sys

from rich import print
from rich.panel import Panel
from rich.table import Table
from csv import writer

from gitgus.deps import config
from gitgus.utils.HTMLStripper import strip_tags


def print_work_item(wi):
    print(f"Work Item: [{config.get('GUS.style.work_id')}]{wi.name}[/{config.get('GUS.style.work_id')}]")
    print(f"Subject:   [{config.get('GUS.style.subject')}]{wi.subject}[/{config.get('GUS.style.subject')}]")
    print(f"Assignee:  [{config.get('GUS.style.assignee')}]{wi.assignee_name}[/{config.get('GUS.style.assignee')}]")
    print(f"Status:    [{config.get('GUS.style.status')}]{wi.status}[/{config.get('GUS.style.status')}]")
    print(f"URL:       [{config.get('GUS.style.url')}]{wi.web_url}[/{config.get('GUS.style.url')}]")
    print(
        f"Build:     [{config.get('GUS.style.build')}]{wi.scheduled_build_name}({wi.scheduled_build})[/{config.get('GUS.style.build')}]"
    )

    print(Panel(strip_tags(wi.details or wi.details_and_steps_to_reproduce), title="Details:"))


def print_prs(res):
    for pr in res:
        print_pr(pr)


def print_pr(pr):
    print(f"- {pr.title} - {pr.html_url}")
    for reviewers in pr.requested_reviewers:
        print(f"  - {reviewers.login}")


def print_wi_table(res, fields=None):
    if fields is None:
        fields = ["work_id_and_subject", "status", "priority", "epic_name"]
    table = Table(header_style=config.get("GUS.style.table_header"))
    for field in fields:
        header_name = field.replace("_", " ").title()
        table.add_column(header_name, max_width=50)
    table.add_column("URL", width=54)
    for wi in res:
        url = "https://gus.my.salesforce.com/apex/ADM_WorkLocator?bugorworknumber=" + wi.name
        vals = [getattr(wi, field) for field in fields]
        vals.append(url)
        table.add_row(*vals)
    print(table)


def print_wi_csv(file_name: str, tickets: list, fields: list = None):
    if fields is None:
        fields = ["work_id_and_subject", "status", "priority", "epic"]
    with open(file_name, "w") as f:
        w = writer(f)
        headers = [f.replace("_", " ").title() for f in fields]
        w.writerow(headers)

        for ticket in tickets:
            if isinstance(ticket, dict):
                vals = [ticket[field] for field in fields]
            else:  # assuming object
                vals = [getattr(ticket, field) for field in fields]
            w.writerow(vals)

import os
import sys
import threading
from datetime import datetime, timedelta
from typing import Callable

import PySimpleGUI as gui
from gitgus.deps import config, work_items, external_editor, git_repo, jenki
from gitgus.workflows.gus_wf import GusWorkflow
from gitgus.utils.console_writer import print_wi_csv
from gitgus.workflows.flaky_wf import FlakyWorkflow

gus_wf = GusWorkflow(config, work_items, external_editor, git_repo)
flaky_wf = FlakyWorkflow(config, work_items, jenki, git_repo)


def get_file_name(extention=".csv", file_types=(("CSV Files", "*.csv"),)):
    filename = gui.popup_get_file(
        "Select a file",
        no_window=True,
        file_types=file_types,
        default_extension=extention,
        save_as=True,
    )
    return filename


def write_csv(data, headers):
    file_name = get_file_name()
    if not file_name:
        return
    print_wi_csv(
        file_name,
        data,
        headers
    )


def working_dlg(is_done: Callable[[], bool]):
    return  # TODO: figure this out
    # layout = [
    #     [gui.Text("Working... Please wait... This probably looks frozen, but multithreading in python is painful...")],
    #     [gui.Button("Cancel")],
    # ]
    # window = gui.Window("Working", layout)
    #
    # def _working_dlg():
    #     while not is_done():
    #         event, values = window.read(timeout=100)
    #         if event == "Cancel" or event == gui.WIN_CLOSED:
    #             window.close()
    #             break
    #     window.close()
    # threading.Thread(target=_working_dlg).start()


def sort_tickets_dlg():
    layout = [
        [gui.Text("Update Tickets")],
        [gui.Text("Team Name (partial okay)"), gui.InputText(default_text="gears")],
        [gui.Text("Release Name"), gui.InputText(default_text="248")],
        [gui.Text("Create report, but do not update tickets"), gui.Checkbox("Dry Run")],
        [gui.Button("Do It"), gui.Button("Cancel")],
    ]
    window = gui.Window("Sort Tickets", layout)
    while 1:
        event, values = window.read()
        if event == "Cancel" or event == gui.WIN_CLOSED:
            window.close()
            break
        elif event == "Do It":
            team_name = values[0]
            release_name = values[1]
            dry_run = values[2]
            tickets = gus_wf.sort_tickets(
                team_name,
                release_name,
                dry_run,
            )
            for ticket in tickets:
                ticket["url"] = "https://gus.my.salesforce.com/apex/ADM_WorkLocator?bugorworknumber=" + ticket["name"]
            write_csv(tickets, ["work_id_and_subject", "status", "priority", "epic", "priority_rank", "old_rank", "url"])
            window.close()
            break


def report_all_builds_dlg():
    end_of_last_month = datetime.now().replace(day=1) - timedelta(days=1)
    start_of_last_month = end_of_last_month.replace(day=1)
    layout = [
        [gui.Text("Report on Builds")],
        [gui.Text("Job Name Like"), gui.InputText(key="job_name_like", default_text="evergage-product")],
        [gui.Text("Start Date"), gui.InputText(key="start_date", default_text=start_of_last_month.strftime("%Y-%m-%d")),
         gui.CalendarButton("📅", close_when_date_chosen=True, target="start_date", format='%Y-%m-%d', size=(10,1))],
        [gui.Text("End Date"), gui.InputText(key="end_date", default_text=end_of_last_month.strftime("%Y-%m-%d")),
         gui.CalendarButton("📅", close_when_date_chosen=True, target="end_date", format='%Y-%m-%d', size=(10,1))],
        [gui.Button("Do It"), gui.Button("Cancel")],
    ]
    window = gui.Window("Report on Builds", layout)
    while 1:
        event, values = window.read()
        if event == "Cancel" or event == gui.WIN_CLOSED:
            window.close()
            break
        elif event == "Do It":
            job_name_like = values["job_name_like"]
            start_date = datetime.strptime(values["start_date"], "%Y-%m-%d")
            end_date = datetime.strptime(values["end_date"], "%Y-%m-%d")

            is_done = False
            working_dlg(lambda: is_done)
            all_results_count, job_result_count = flaky_wf.build_report(job_name_like, start_date, end_date)
            is_done = True

            file_name = get_file_name()
            with open(file_name, "w") as f:
                f.write(f"Results between {start_date} and {end_date}\n")
                total = sum(all_results_count.values())
                f.write(f"Total builds: {total}\n")
                for k, v in all_results_count.items():
                    f.write(f"{k}: {v} %{round(v/total*100, 2)}\n")

                for job, counts in job_result_count.items():
                    f.write(f"\n{job}\n")
                    total = sum(counts.values())
                    for k, v in counts.items():
                        f.write(f"{k}: {v} %{round(v/total*100, 2)}\n")
            window.close()


def app():
    layout = [
        [
            gui.Frame(
                "What do you want to do?",
                layout=[
                    [gui.Column(layout=[
                        [gui.Text("Sort the team's tickets priorities to (hopefully) match our desired priorities")],
                        [gui.Text("Get a report on how all the recent builds have gone, noting failures and successes")],
                        [gui.Text("Get a report on flakies from the recent past.")],
                    ]),
                    gui.Column(layout=[
                        [gui.Button("Sort Tickets")],
                        [gui.Button("Report on Builds")],
                        [gui.Button("Report on Flakies")],
                    ])]
                ],
            )
        ],
        [gui.Button("Close")],
    ]

    window = gui.Window("gitgus", layout)

    while 1:
        event, values = window.read()
        if event == "Close" or event == gui.WIN_CLOSED:
            break
        elif event == "Sort Tickets":
            sort_tickets_dlg()
        elif event == "Report on Builds":
            report_all_builds_dlg()
        elif event == "Report on Flakies":
            gui.popup("TODO")

    # Finish up by removing from the screen
    window.close()


if __name__ == "__main__":
    # print version
    if len(sys.argv) >= 2 and sys.argv[1] == "--version":
        import importlib.metadata

        my_version = importlib.metadata.version("gitgus")
        print("gitgus version: " + my_version)
        sys.exit(0)
    app()

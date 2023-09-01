import PySimpleGUI as gui
from gitgus.deps import config, work_items, external_editor, git_repo
from gitgus.workflows.gus_wf import GusWorkflow
from gitgus.utils.console_writer import print_wi_csv

gus_wf = GusWorkflow(config, work_items, external_editor, git_repo)


def get_file_name():
    filename = gui.popup_get_file(
        "Select a file",
        no_window=True,
        file_types=(("CSV Files", "*.csv"),),
        default_extension="*.csv",
        save_as=True,
    )
    return filename


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
            file_name = get_file_name()
            for ticket in tickets:
                ticket["url"] = "https://gus.my.salesforce.com/apex/ADM_WorkLocator?bugorworknumber=" + ticket["name"]
            print_wi_csv(
                file_name,
                tickets,
                ["work_id_and_subject", "status", "priority", "epic", "priority_rank", "old_rank", "url"],
            )
            window.close()
            break


def app():
    layout = [
        [
            gui.Frame(
                "What do you want to do?",
                layout=[
                    [
                        # TODO - figure out columns to align buttons
                        gui.Text("Sort the team's tickets priorities to (hopefully) match our desired priorities"),
                        gui.Button("Sort Tickets"),
                    ],
                    [
                        gui.Text("Get a report on how all the recent builds have gone, noting failures and successes"),
                        gui.Button("Report on Builds"),
                    ],
                    [
                        gui.Text("Get a report on flakies from the recent past."),
                        gui.Button("Report on Flakies"),
                    ],
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
            gui.popup("TODO")
        elif event == "Report on Flakies":
            gui.popup("TODO")

    # Finish up by removing from the screen
    window.close()


if __name__ == "__main__":
    app()

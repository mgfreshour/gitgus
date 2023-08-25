import PySimpleGUI as gui
from gitgus.gus.sobjects.work import Work


def app():
    wi = Work.get_by_name("W-12550086")

    layout = [
        [gui.Text("What's your name?")],
        [gui.Input(default_text=wi.epic_name, key="name")],
        [gui.Button("Ok"), gui.Button("Close")],
    ]

    window = gui.Window("Window Title", layout)

    while 1:
        event, values = window.read()
        if event == "Close" or event == gui.WIN_CLOSED:
            break

    # Finish up by removing from the screen
    window.close()


if __name__ == "__main__":
    app()

from rich import print
from rich.prompt import Prompt

from gitgus.utils.menu import get_choice
from gitgus.deps import teams


def choose_one(prompt, search_fn, default=""):
    name = Prompt.ask(prompt, default=default)
    if not name:
        print("No name provided. Skipping.")
        return None
    objects = list(search_fn(name))
    if len(objects) == 0:
        print(
            f"No objects found for {name}. "
            "Skipping. You can manually add it to the config file or run gitgus config init again"
        )
        return None
    if len(objects) == 1:
        return objects[0]
    return objects[get_choice([o.name for o in objects])]


def choose_gus_team():
    return choose_one(
        "What is your GUS Team Name? (partial okay)",
        search_fn=lambda n: teams.get_team(n),
    )

import os
from gitgus.git_repo import GitRepo
from gitgus.gh import GH
from gitgus.gus.workitems import WorkItems
from gitgus.gus.builds import Builds
from gitgus.gus.teams import Teams
from gitgus.gus.products import Products
from gitgus.utils.external_editor import ExternalEditor
from gitgus.config import instance
from gitgus.jenki import Jenki

config = instance()
external_editor = ExternalEditor(
    os.environ["EDITOR"] if "EDITOR" in os.environ else "vim"
)
git_repo = GitRepo()
work_items = WorkItems()
gh = GH(config.get("github.token"))
jenki = Jenki(config)
builds = Builds()
teams = Teams()
products = Products()

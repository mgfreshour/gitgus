import typer
from rich import print

from .command_release import release_app
from .command_pr import pr_app
from .command_gus import gus_app, _checkout
from .command_config import config_app
from .command_flaky import flaky_app
from .command_dev import dev_app

app = typer.Typer(no_args_is_help=True, pretty_exceptions_show_locals=False)

app.add_typer(dev_app, name="dev", help="Commands for developing gitgus.", no_args_is_help=True)
app.add_typer(
    flaky_app,
    name="flaky",
    help="Commands for working with flaky tests.",
    no_args_is_help=True,
)
app.add_typer(
    pr_app,
    name="pr",
    help="Commands for working with PRs in the present directory's remote 'origin' repo.",
    no_args_is_help=True,
)
app.add_typer(
    pr_app,
    name="prs",
    help="Commands for working with PRs in the present directory's remote 'origin' repo.",
    no_args_is_help=True,
    hidden=True,
)
app.add_typer(gus_app, name="gus", help="Commands for working with GUS.", no_args_is_help=True)
app.add_typer(
    config_app,
    name="config",
    help="Commands for working with the config.",
    no_args_is_help=True,
)
app.add_typer(
    release_app,
    name="release",
    help="Commands for working with releases.",
    no_args_is_help=True,
)


# Shortcut for most used commands. TODO - figure out how to do this without duplicating.
@app.command()
def checkout(mark_ip: bool = typer.Option(True, "--ip/--no-ip", "-m/-M", help="Mark ticket as in progress")):
    """Checkout a branch for a ticket. Alias: co"""
    _checkout(mark_ip)


@app.command()
def co(mark_ip: bool = typer.Option(True, "--ip/--no-ip", "-m/-M", help="Mark ticket as in progress"), hidden=True):
    """Checkout a branch for a ticket."""
    _checkout(mark_ip)


@app.command()
def version():
    """Print the version. Read from pyproject.toml."""
    import importlib.metadata

    my_version = importlib.metadata.version("gitgus")
    print(my_version)


@app.command()
def gui():
    from .gui import app as gui_app

    gui_app()


if __name__ == "__main__":
    app()

import os

import typer


from gitgus.dev.sobject_description import SObjectDescription
from jinja2 import Environment, PackageLoader, select_autoescape

from gitgus.gus.sobjects.work import Work
from gitgus.gus.gus_client import GUSClient

dev_app = typer.Typer(no_args_is_help=True)

env = Environment(
    loader=PackageLoader("gitgus"),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)


def validate_python_code(code: str):
    try:
        compile(code, "<string>", "exec")
    except SyntaxError as e:
        print(code)
        raise e


def black_format(code: str):
    import black

    mode = black.Mode()
    mode.line_length = 120
    return black.format_str(code, mode=mode)


def write_sobject(sobject: SObjectDescription, out_dir: str):
    template = env.get_template("sobject.py.jinja2")

    out = template.render(
        sobject=sobject,
        field_names=[x.name_snakecase for x in sobject.fields_all],
        enumerate=enumerate,
        fields_config={
            x.name_snakecase: {"alias": x.name, "title": x.label}
            for x in sobject.fields_all
        },
        fields_queryable_config={
            x.name_snakecase: {"alias": x.name, "title": x.label}
            for x in sobject.fields_queryable
        },
        fields_creatable_config={
            x.name_snakecase: {"alias": x.name, "title": x.label}
            for x in sobject.fields_creatable
        },
        import_date=("xsd:date" in (x.soap_type for x in sobject.fields_all)),
        import_enum=any(bool(x.enum_values) for x in sobject.fields_all),
    )
    validate_python_code(out)
    out = black_format(out)
    with open(os.path.join(out_dir, f"{sobject.label_snakecase}.py"), "w") as f:
        f.write(out)


@dev_app.command()
def generate_sobjects(names: list[str]):
    """Generate a new sobject class."""
    gus = GUSClient.instance()

    out_dir = "/Users/mfreshour/src/gitgus/gitgus/gus/sobjects/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not os.path.isdir(out_dir):
        raise Exception(f"{out_dir} is not a directory")

    for name in names:
        desc = gus.sf.__getattr__(name).describe()
        sobject = SObjectDescription(**desc)
        print(f"Writing gus/sobjects/{sobject.label_snakecase}")
        write_sobject(sobject, out_dir)

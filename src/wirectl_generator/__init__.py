import click
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape

from wirectl import load_icd


@click.command()
@click.argument("icd", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option(
    "--output",
    type=click.Path(exists=False, file_okay=False, dir_okay=True, path_type=Path),
    default=Path.cwd(),
    help="output directory for the generated ICD",
)
def cli(icd, output):
    """Generate types from the given ICD YAML file"""

    icd = load_icd(icd)

    env = Environment(
        loader=PackageLoader("wirectl_generator"),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    parameters_path = output / "parameters.py"
    telemetry_path = output / "telemetry.py"
    actions_path = output / "actions.py"

    output.mkdir(parents=True, exist_ok=True)

    template = env.get_template("parameters.py.jinja2")
    rendered = template.render(icd=icd)
    with open(parameters_path, "w") as file:
        file.write(rendered)

    template = env.get_template("telemetry.py.jinja2")
    rendered = template.render(icd=icd)
    with open(telemetry_path, "w") as file:
        file.write(rendered)

    template = env.get_template("actions.py.jinja2")
    rendered = template.render(icd=icd)
    with open(actions_path, "w") as file:
        file.write(rendered)


def main() -> None:
    cli()

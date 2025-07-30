from pathlib import Path
import json

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

import click


def get_bm_config(paramfile: Path, bm_type: str):
    if not paramfile.exists():
        raise FileNotFoundError(f"{paramfile.name} could not be found")
    data = tomllib.loads(paramfile.read_text())
    return "\n".join(data[bm_type])

def get_anyscript_info(anyinfofile:Path):
    if not anyinfofile.exists():
        raise FileNotFoundError(f"{anyinfofile.name} could not be found")
    data =  json.loads(anyinfofile.read_text())
    return "\n".join(data)

@click.command()
@click.option(
    "--ammr",
    type=click.Path(),
    help="AMMR paths.",
)
@click.option(
    "--reference-manual",
    type=click.Path(),
    help="Path to the AMS reference manual",
)
@click.option(
    "--output",
    default=Path(__file__).parent.parent / "src/pygments_anyscript",
    type=click.Path(),
    help="Path to the AMS reference manual",
)
def create_files(ammr: str, reference_manual: str, output:str):
    output = Path(output)
    if ammr:
        bm_paramfile = Path(ammr) / "Body/AAUHuman/bm-parameters.toml"
        with open(output / "BM_constants.txt", "w") as fh:
            fh.write(get_bm_config(bm_paramfile, "constants"))
        with open(output / "BM_parameters.txt", "w") as fh:
            fh.write(get_bm_config(bm_paramfile, "parameters"))

    if reference_manual:
        classes_file = Path(reference_manual) / "_anybody-data/all-classes.json"
        with open(output / "classes.txt", "w") as fh:
            fh.write(get_anyscript_info(classes_file))

        functions_file = Path(reference_manual) / "_anybody-data/all-functions.json"
        with open(output / "functions.txt", "w") as fh:
            fh.write(get_anyscript_info(functions_file))

        globals_file = Path(reference_manual) / "_anybody-data/all-globals.json"
        with open(output / "globals.txt", "w") as fh:
            fh.write(get_anyscript_info(globals_file))



if __name__ == '__main__':
    create_files()
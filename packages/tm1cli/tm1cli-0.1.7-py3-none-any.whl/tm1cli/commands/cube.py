from typing import Annotated

import typer
from rich import print  # pylint: disable=redefined-builtin
from TM1py.Services import TM1Service

from tm1cli.utils.cli_param import DATABASE_OPTION, INTERVAL_OPTION, WATCH_OPTION
from tm1cli.utils.various import resolve_database
from tm1cli.utils.watch import watch_option

app = typer.Typer()


@app.command(name="ls", help="Alias for list")
@app.command(name="list")
def list_cube(
    ctx: typer.Context,
    database: Annotated[str, DATABASE_OPTION] = None,
    skip_control_cubes: Annotated[
        bool,
        typer.Option(
            "-s",
            "--skip-control-cubes",
            help="Flag for not printing control cubes.",
        ),
    ] = False,
):
    """
    List cubes
    """

    with TM1Service(**resolve_database(ctx, database)) as tm1:
        for cube in tm1.cubes.get_all_names(skip_control_cubes):
            print(cube)


@app.command()
@watch_option
def exists(
    ctx: typer.Context,
    cube_name: str,
    database: Annotated[str, DATABASE_OPTION] = None,
    watch: Annotated[bool, WATCH_OPTION] = False,  # pylint: disable=unused-argument
    interval: Annotated[int, INTERVAL_OPTION] = 5,  # pylint: disable=unused-argument
):
    """
    Check if cube exists
    """
    with TM1Service(**resolve_database(ctx, database)) as tm1:
        print(tm1.cubes.exists(cube_name))

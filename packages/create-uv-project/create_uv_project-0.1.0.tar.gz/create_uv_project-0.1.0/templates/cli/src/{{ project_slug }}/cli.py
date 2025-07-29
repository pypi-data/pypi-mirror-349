# src/{{ project_slug }}/cli.py

import typer
from typing_extensions import Annotated # For Typer <0.7.0, use typing_extensions; for >=0.7.0, use typing.Annotated
from typing import Optional

from . import __version__
from .commands import example # Assuming an example subcommand module

app = typer.Typer(
    name="{{ project_slug }}",
    help="{{ project_description | default('A cool CLI application built with Typer.') }}",
    add_completion=False, # Disable shell completion for simplicity, can be enabled
)

# Add subcommands from other modules
app.add_typer(example.app, name="example", help="Example commands.")


def version_callback(value: bool):
    if value:
        typer.echo(f"{{ project_name }} CLI Version: {__version__}")
        raise typer.Exit()

@app.callback()
def main(
    ctx: typer.Context,
    version: Annotated[
        Optional[bool],
        typer.Option("--version", "-v", callback=version_callback, is_eager=True, help="Show application version and exit.")
    ] = None,
):
    """
    {{ project_name }}: A modern CLI application.
    """
    # This main callback can be used for global options or setup
    # typer.echo(f"CLI App: {{ project_name }} running.")
    # If no command is given, Typer will show help by default.
    pass

# It's common for the Typer app instance to be the main export for the script entry point.
# The `if __name__ == "__main__":` block is less common with Typer if using console_scripts,
# as Typer handles the execution flow when called as a script. 
# src/{{ project_slug }}/commands/example.py # Renamed from example_command.py

import typer
from typing_extensions import Annotated
from typing import Optional

app = typer.Typer(
    name="example", 
    help="An example command suite.",
    no_args_is_help=True # Show help if no subcommand is given for this Typer app
)

@app.command()
def hello(
    name: Annotated[Optional[str], typer.Option(help="The person to greet.")] = None,
    formal: Annotated[bool, typer.Option(help="Use a formal greeting.")] = False,
):
    """
    Greets a person.
    """
    if name:
        message = f"How do you do, {name}?" if formal else f"Hey {name}!"
    else:
        message = "Salutations!" if formal else "Hello there!"
    
    typer.secho(message, fg=typer.colors.BRIGHT_GREEN)
    typer.echo("This is an example command from the 'example' subcommand suite.")

@app.command()
def goodbye(
    name: Annotated[str, typer.Argument(help="The name to say goodbye to.")] = "World",
    show_time: Annotated[bool, typer.Option("--show-time", "-t", help="Show the current time with the goodbye message.")] = False,
):
    """
    Says goodbye to NAME.
    """
    message = f"Farewell, {name}!"
    if show_time:
        import datetime
        message += f" The time is now {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
    
    typer.secho(message, fg=typer.colors.BRIGHT_MAGENTA)

# To add more commands to this "example" suite, just define them with @app.command() 
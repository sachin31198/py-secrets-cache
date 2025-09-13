"""Console script for secrets_cache."""

import typer
from rich.console import Console


app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for secrets_cache."""
    console.print("Replace this message by putting your code into "
               "secrets_cache.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    # utils.do_something_useful()


if __name__ == "__main__":
    app()

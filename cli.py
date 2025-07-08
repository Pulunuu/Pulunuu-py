# cli.py
import typer
from commands import init, install, run, add, remove

app = typer.Typer()

app.command(name="init")(init.main)
app.command(name="install")(install.main)
app.command(name="add")(add.main)
app.command(name="remove")(remove.main)

app.command(name="run")(run.main)

if __name__ == "__main__":
    app()

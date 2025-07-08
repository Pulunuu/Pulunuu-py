import typer
from rich.console import Console
from core.json_io import load_py_json, save_py_json, save_pylock_json
from core.deps import pip_install
from core.lock import generate_lock_data

console = Console()
app = typer.Typer()

@app.command()
def main(pkg: str):
    console.print(f"[cyan]➕ Adding {pkg}...[/cyan]")

    config = load_py_json()

    if pkg in config.dependencies:
        console.print(f"[yellow]{pkg} already in py.json[/yellow]")
        return

    config.dependencies[pkg] = "*"
    save_py_json(config)

    try:
        pip_install(pkg)
    except Exception:
        console.print(f"[red]Failed to install {pkg}[/red]")
        return

    lock_data = generate_lock_data(config)
    save_pylock_json(lock_data)
    console.print(f"[bold green]✅ {pkg} added and locked[/bold green]")


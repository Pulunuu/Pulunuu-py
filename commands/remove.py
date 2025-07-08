
import typer
from rich.console import Console
from core.json_io import load_py_json, save_py_json, save_pylock_json
from core.deps import pip_uninstall
from core.lock import generate_lock_data

console = Console()
app = typer.Typer()

@app.command()
def main(pkg: str):
    console.print(f"[cyan]➖ Removing {pkg}...[/cyan]")

    config = load_py_json()
    if pkg not in config.dependencies:
        console.print(f"[yellow]{pkg} not found in py.json[/yellow]")
        return

    del config.dependencies[pkg]
    save_py_json(config)

    try:
        pip_uninstall(pkg)
    except Exception:
        console.print(f"[red]Failed to uninstall {pkg}[/red]")
        return

    lock_data = generate_lock_data(config)
    save_pylock_json(lock_data)
    console.print(f"[bold green]✅ {pkg} removed and lock updated[/bold green]")


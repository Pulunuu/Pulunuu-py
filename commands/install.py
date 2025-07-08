# commands/install.py

import subprocess
import sys
import json
from pathlib import Path
from rich.console import Console
from core.parser import PyConfig
from core.venv import ensure_venv
from core.lock import generate_lock_data
from core.json_io import save_pylock_json
import typer
app = typer.Typer()
console = Console()

@app.command()
def main():
    config_path = Path("py.json")
    if not config_path.exists():
        console.print("[bold red]py.json not found. Run `pylock init` first.[/bold red]")
        sys.exit(1)

    with open(config_path) as f:
        config = PyConfig(**json.load(f))

    venv_python = ensure_venv()

    deps = [f"{name}" for name in config.dependencies.keys()]
    if not deps:
        console.print("[yellow]No dependencies specified in py.json[/yellow]")
    else:
        console.print(f"[cyan]📦 Installing dependencies:[/cyan] {' '.join(deps)}")
        subprocess.run([venv_python, "-m", "pip", "install"] + deps, check=True)

    lock_data = generate_lock_data(config)
    save_pylock_json(lock_data)
    console.print("[bold green]✅ Dependencies installed and pylock.json generated.[/bold green]")



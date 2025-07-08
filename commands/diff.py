# commands/diff.py

import subprocess
import json
import sys
import typer
from rich.console import Console
from typing import Dict, List
from pathlib import Path

console = Console()
app = typer.Typer()

def get_current_packages() -> Dict[str, str]:
    result = subprocess.run(
        [".venv/bin/python", "-m", "pip", "freeze"],
        capture_output=True,
        text=True,
        check=True
    )
    lines = result.stdout.strip().splitlines()
    return {line.split("==")[0].lower(): line.split("==")[1] for line in lines if "==" in line}

def get_locked_packages(full_meta=False) -> Dict[str, str]:
    if not Path("pulumuu.lock.json").exists():
        console.print("[red]pulumuu.lock.json not found.[/red]")
        sys.exit(1)

    with open("pulumuu.lock.json") as f:
        lock = json.load(f)
    deps = lock.get("dependencies", {})
    if full_meta:
        return {name.lower(): meta for name, meta in deps.items()}
    else:
        return {name.lower(): meta["version"] for name, meta in deps.items()}

def run_pip(args: List[str]):
    console.print(f"[cyan]$ pip {' '.join(args)}[/cyan]")
    subprocess.run([".venv/bin/python", "-m", "pip"] + args, check=True)

@app.command()
def main(
    json_output: bool = typer.Option(False, "--json", help="Output result as JSON"),
    fix: bool = typer.Option(False, "--fix", help="Automatically fix environment to match lock")
):
    current = get_current_packages()
    locked = get_locked_packages()
    locked_meta = get_locked_packages(full_meta=True)

    missing = []
    extra = []
    mismatch = []

    for name, version in locked.items():
        if name not in current:
            missing.append({"name": name, "locked": version})
        elif current[name] != version:
            mismatch.append({"name": name, "locked": version, "current": current[name]})

    for name, version in current.items():
        if name not in locked:
            extra.append({"name": name, "current": version})

    has_diff = bool(missing or mismatch or extra)

    if fix:
        if not has_diff:
            console.print("[green]✅ No fixes needed.[/green]")
            sys.exit(0)

        console.print("[yellow]🔧 Fixing environment to match pulumuu.lock.json...[/yellow]")
        for pkg in mismatch:
            run_pip(["install", f"{pkg['name']}=={pkg['locked']}"])
        for pkg in missing:
            run_pip(["install", f"{pkg['name']}=={pkg['locked']}"])
        for pkg in extra:
            run_pip(["uninstall", "-y", pkg["name"]])
        console.print("[green]✅ Environment fixed.[/green]")
        sys.exit(0)

    if json_output:
        output = {
            "missing": missing,
            "mismatch": mismatch,
            "extra": extra
        }
        print(json.dumps(output, indent=2))
    else:
        if missing:
            console.print("⚠️ [yellow]Missing packages:[/yellow]")
            for pkg in missing:
                console.print(f"  - {pkg['name']} (locked: {pkg['locked']})")
        if mismatch:
            console.print("🔴 [red]Version mismatches:[/red]")
            for pkg in mismatch:
                console.print(f"  - {pkg['name']} (locked: {pkg['locked']}, current: {pkg['current']})")
        if extra:
            console.print("🟡 [cyan]Extra packages:[/cyan]")
            for pkg in extra:
                console.print(f"  - {pkg['name']} (current: {pkg['current']})")

        if not has_diff:
            console.print("[bold green]✅ No differences. Environment matches lock file.[/bold green]")

    sys.exit(1 if has_diff else 0)

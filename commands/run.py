# commands/init.py

import json
from pathlib import Path
from rich.console import Console
from core.parser import PyConfig  # ← pydantic schemaを定義したファイル

console = Console()

DEFAULT_CONFIG = {
    "name": "my-project",
    "description": "An AI-ready FastAPI backend",
    "entry": "app.py",
    "scripts": {
        "dev": "pulumuu run app.py"
    },
    "dependencies": {
        "fastapi": "^0.110.0",
        "openai": "^1.12.0"
    },
    "models": {
        "openai:gpt-4": {
            "provider": "openai",
            "id": "gpt-4",
            "context": "8k",
            "version": "4.0.0"
        }
    },
    "env": {
        "default": "dev",
        "environments": {
            "dev": {
                "PYTHON_ENV": "development"
            },
            "prod": {
                "PYTHON_ENV": "production"
            }
        }
    },
    "lock": {
        "strict": True
    }
}

def main():
    path = Path("pulumuu.json")
    if path.exists():
        console.print("[bold red]pulumuu.json already exists.[/bold red]")
        return

    try:
        config = PyConfig(**DEFAULT_CONFIG)
        with open(path, "w") as f:
            json.dump(config.dict(), f, indent=2)
        console.print("[bold green]✨ pulumuu.json has been created.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Failed to generate pulumuu.json:[/bold red] {e}")

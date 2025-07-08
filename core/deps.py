# core/deps.py

import subprocess
from core.venv import ensure_venv

def pip_install(package: str):
    python = ensure_venv()
    subprocess.run([python, "-m", "pip", "install", package], check=True)

def pip_uninstall(package: str):
    python = ensure_venv()
    subprocess.run([python, "-m", "pip", "uninstall", "-y", package], check=True)

def get_frozen_packages() -> list[str]:
    python = ensure_venv()
    result = subprocess.run(
        [python, "-m", "pip", "freeze"],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip().splitlines()

# core/venv.py

import os
import sys
import subprocess
from pathlib import Path

def ensure_venv():
    venv_dir = Path(".venv")
    if not venv_dir.exists():
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)

    if sys.platform == "win32":
        return str(venv_dir / "Scripts" / "python.exe")
    else:
        return str(venv_dir / "bin" / "python")

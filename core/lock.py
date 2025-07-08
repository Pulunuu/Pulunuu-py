# core/lock.py

import subprocess
import platform
import sys
from datetime import datetime
from core.parser import PyConfig
from typing import Dict


def generate_lock_data(config: PyConfig) -> Dict:
    """
    Generate a structured pylock.json format
    """
    # 1. pip freeze to get current packages
    result = subprocess.run([
        ".venv/bin/python", "-m", "pip", "freeze"
    ], capture_output=True, text=True, check=True)

    frozen_lines = result.stdout.strip().splitlines()
    
    # 2. Parse into structured dependencies
    direct_deps = set(config.dependencies.keys())
    deps = {}
    for line in frozen_lines:
        if "==" not in line:
            continue
        name, version = line.strip().split("==")
        deps[name] = {
            "version": version,
            "transitive": name not in direct_deps,
            "source": "pypi",
            "resolved": f"https://pypi.org/project/{name}/{version}/"
        }

    # 3. Build lock dict
    lock = {
        "dependencies": deps,
"models": {k: v.dict() for k, v in config.models.items()} if config.models else {},
        "env": config.env.dict() if config.env else {},
        "meta": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "platform": platform.platform(),
            "python": platform.python_version(),
            "pylock_version": "0.1.3"
        }
    }

    return lock

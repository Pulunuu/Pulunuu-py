# core/json_io.py

import json
from pathlib import Path
from core.parser import PyConfig

def load_py_json():
    with open("py.json") as f:
        return PyConfig(**json.load(f))

def save_py_json(config: PyConfig):
    with open("py.json", "w") as f:
        json.dump(config.dict(), f, indent=2)

def save_pylock_json(lock_data: dict):
    with open("pylock.json", "w") as f:
        json.dump(lock_data, f, indent=2)

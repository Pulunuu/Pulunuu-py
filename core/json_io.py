# core/json_io.py

import json
from pathlib import Path
from core.parser import PyConfig

def load_pulumuu_json():
    with open("pulumuu.json") as f:
        return PyConfig(**json.load(f))

def save_pulumuu_json(config: PyConfig):
    with open("pulumuu.json", "w") as f:
        json.dump(config.dict(), f, indent=2)  # 修正: dict() にして正しく保存

def save_pulumuu_lock_json(lock_data: dict):
    with open("pulumuu.lock.json", "w") as f:
        json.dump(lock_data, f, indent=2)

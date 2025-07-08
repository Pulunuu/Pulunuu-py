# core/utils.py

import re

def convert_npm_semver_to_pip(ver: str) -> str:
    if ver.startswith("^"):
        base = ver[1:]
        parts = base.split(".")
        if len(parts) == 3:
            major, minor, patch = map(int, parts)
            if major > 0:
                return f">={major}.{minor}.{patch},<{major+1}.0.0"
            elif minor > 0:
                return f">={major}.{minor}.{patch},<{major}.{minor+1}.0"
            else:
                return f">={major}.{minor}.{patch},<{major}.{minor}.{patch+1}"
        return base  # fallback
    return ver  # already pip-compatible

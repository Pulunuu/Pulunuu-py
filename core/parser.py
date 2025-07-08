# core/parser.py

from pydantic import BaseModel
from typing import Dict, Optional

class ModelSpec(BaseModel):
    provider: str
    id: str
    version: Optional[str]
    context: Optional[str]

class EnvSpec(BaseModel):
    default: str
    environments: Dict[str, Dict[str, str]]

class PyConfig(BaseModel):
    name: str
    description: Optional[str]
    entry: Optional[str]
    scripts: Dict[str, str]
    dependencies: Dict[str, str]
    models: Optional[Dict[str, ModelSpec]]
    env: Optional[EnvSpec]
    lock: Optional[Dict[str, bool]]

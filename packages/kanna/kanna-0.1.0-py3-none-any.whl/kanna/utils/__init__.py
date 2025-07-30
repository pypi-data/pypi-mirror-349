from pathlib import Path
from typing import TypedDict, cast

import tomli


class CommandConfig(TypedDict):
    command: str
    help: str | None
    pre: list[str] | None
    post: list[str] | None

type Command = str | CommandConfig

class KannaConfig(TypedDict):
    tasks: dict[str, Command]

def load_config_from_project() -> KannaConfig:
    pyproject = Path('pyproject.toml')

    if not pyproject.exists():
        raise FileNotFoundError("Initialize a pyproject before calling Kanna")
    
    config_data: KannaConfig | None = None

    with pyproject.open('rb') as config:
        config_data = cast(KannaConfig, tomli.load(config).get('tool', {}).get('kanna'))

    return config_data or {}
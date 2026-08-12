import tomllib
from pathlib import Path
from typing import Any

CONFIG_FILE = Path(__file__).parent.parent / "config" / "config.toml"

def load_config() -> dict[str, Any]:
    """
    Load configuration from a TOML file.
    """
    with CONFIG_FILE.open("rb") as f:
        return tomllib.load(f)

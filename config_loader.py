"""config_loader.py — validated settings loader for Fiber EUR v1.5."""
from __future__ import annotations

import json
from pathlib import Path

DEFAULT_SETTINGS_PATH = Path(__file__).parent / "settings.json"


def load_json_settings(path: str | Path = DEFAULT_SETTINGS_PATH) -> dict:
    with open(path) as f:
        return json.load(f)

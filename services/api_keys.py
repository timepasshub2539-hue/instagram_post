import os
import json

SETTINGS_PATH = "data/settings.json"


def _load_settings() -> dict:
    try:
        with open(SETTINGS_PATH) as f:
            return json.load(f)
    except Exception:
        return {}


def get_key(env_var: str, settings_field: str) -> str | None:
    """Return env var if set, otherwise fall back to value stored in settings.json."""
    return os.getenv(env_var) or _load_settings().get(settings_field) or None

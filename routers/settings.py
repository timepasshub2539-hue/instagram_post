import os
import json
import requests
from fastapi import APIRouter

router = APIRouter()
SETTINGS_PATH = "data/settings.json"

DEFAULTS = {
    "ai_mode": "online",
    "ollama_model": "llama3",
    "openai_model": "gpt-4o-mini",
    "mistral_model": "mistral-small-latest",
    "lmstudio_model": "local-model",
    "lmstudio_url": "http://localhost:1234/v1",
    "default_theme": "dark",
    "default_font": "DMSans",
    "instagram_handle": "",
    "posting_time_1": "06:00",
    "posting_time_2": "21:00",
    "niche": "",
    "onboarding_complete": False,
}


def _load() -> dict:
    try:
        with open(SETTINGS_PATH) as f:
            return json.load(f)
    except Exception:
        return {}


def _save(data: dict):
    os.makedirs("data", exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(data, f, indent=2)


def _ping(url: str) -> bool:
    try:
        return requests.get(url, timeout=2).status_code == 200
    except Exception:
        return False


@router.get("/settings")
def get_settings():
    data = {**DEFAULTS, **_load()}

    lmstudio_url = data.get("lmstudio_url", "http://localhost:1234/v1")

    return {
        **data,
        "claude_available":   bool(os.getenv("ANTHROPIC_API_KEY")),
        "openai_available":   bool(os.getenv("OPENAI_API_KEY")),
        "mistral_available":  bool(os.getenv("MISTRAL_API_KEY")),
        "ollama_available":   _ping(f"{os.getenv('OLLAMA_BASE_URL','http://localhost:11434')}/api/tags"),
        "lmstudio_available": _ping(f"{lmstudio_url}/models"),
    }


@router.post("/settings")
def update_settings(body: dict):
    current = {**DEFAULTS, **_load()}
    current.update(body)
    _save(current)
    return {"success": True, "settings": current}

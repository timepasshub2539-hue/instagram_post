import os
import json
import requests
from services.ai_claude import generate_with_claude
from services.ai_ollama import generate_with_ollama
from services.ai_openai_svc import generate_with_openai
from services.ai_lmstudio import generate_with_lmstudio
from services.ai_mistral import generate_with_mistral


def _load_settings() -> dict:
    try:
        with open("data/settings.json") as f:
            return json.load(f)
    except Exception:
        return {}


def is_ollama_available() -> bool:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    try:
        return requests.get(f"{base_url}/api/tags", timeout=2).status_code == 200
    except Exception:
        return False


def is_lmstudio_available(base_url: str = None) -> bool:
    url = base_url or os.getenv("LMSTUDIO_URL", "http://localhost:1234/v1")
    try:
        return requests.get(f"{url}/models", timeout=2).status_code == 200
    except Exception:
        return False


def generate_carousel(mood: str, user_context: str, ai_mode: str) -> dict:
    settings = _load_settings()

    if ai_mode == "online":
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("Add your Claude API key in Settings to use online mode")
        return generate_with_claude(mood, user_context)

    elif ai_mode == "openai":
        model = settings.get("openai_model", "gpt-4o-mini")
        return generate_with_openai(mood, user_context, model=model)

    elif ai_mode == "mistral":
        model = settings.get("mistral_model", "mistral-small-latest")
        return generate_with_mistral(mood, user_context, model=model)

    elif ai_mode == "lmstudio":
        model = settings.get("lmstudio_model", "local-model")
        base_url = settings.get("lmstudio_url", os.getenv("LMSTUDIO_URL", "http://localhost:1234/v1"))
        return generate_with_lmstudio(mood, user_context, model=model, base_url=base_url)

    elif ai_mode == "local":
        model = settings.get("ollama_model", "llama3")
        return generate_with_ollama(mood, user_context, model=model)

    else:
        raise ValueError(f"Unknown AI mode: {ai_mode}")

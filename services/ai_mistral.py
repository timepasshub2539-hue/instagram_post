import json
from openai import OpenAI, AuthenticationError, RateLimitError
from services.prompts import build_prompt
from services.api_keys import get_key

MISTRAL_BASE_URL = "https://api.mistral.ai/v1"


def generate_with_mistral(mood: str, user_context: str, model: str = "mistral-small-latest") -> dict:
    api_key = get_key("MISTRAL_API_KEY", "mistral_api_key")
    if not api_key:
        raise ValueError("Add your Mistral API key in Settings to use Mistral")

    # Mistral exposes an OpenAI-compatible endpoint
    client = OpenAI(base_url=MISTRAL_BASE_URL, api_key=api_key)
    prompt_text = build_prompt(mood, user_context)

    for attempt in range(2):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt_text}],
                max_tokens=1024,
                temperature=0.9,
            )
            raw = resp.choices[0].message.content.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            return json.loads(raw)
        except json.JSONDecodeError:
            if attempt == 1:
                raise RuntimeError("Generation failed, tap to retry")
        except AuthenticationError:
            raise ValueError("Invalid Mistral API key. Check Settings.")
        except RateLimitError:
            raise RuntimeError("Mistral rate limit hit, try again in a moment")

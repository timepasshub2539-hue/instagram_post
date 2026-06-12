import json
import anthropic
from services.prompts import build_prompt
from services.api_keys import get_key


def generate_with_claude(mood: str, user_context: str) -> dict:
    api_key = get_key("ANTHROPIC_API_KEY", "anthropic_api_key")
    if not api_key:
        raise ValueError("Add your Claude API key in Settings to use online mode")

    client = anthropic.Anthropic(api_key=api_key)
    prompt_text = build_prompt(mood, user_context)

    for attempt in range(2):
        try:
            message = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                temperature=1.0,
                messages=[{"role": "user", "content": prompt_text}]
            )
            raw = message.content[0].text.strip()
            # Strip markdown code fences if model wraps anyway
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            return json.loads(raw)
        except json.JSONDecodeError:
            if attempt == 1:
                raise RuntimeError("Generation failed, tap to retry")
        except anthropic.RateLimitError:
            raise RuntimeError("Claude is busy, try again in a moment or switch to Local mode")
        except anthropic.AuthenticationError:
            raise ValueError("Add your Claude API key in Settings to use online mode")
        except anthropic.APIStatusError as e:
            raise RuntimeError(f"Claude API error {e.status_code}: {e.message}")

import os
import json
from openai import OpenAI, AuthenticationError, RateLimitError
from services.prompts import build_prompt


def generate_with_openai(mood: str, user_context: str, model: str = "gpt-4o-mini") -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Add your OpenAI API key in Settings to use OpenAI")

    client = OpenAI(api_key=api_key)
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
            raise ValueError("Invalid OpenAI API key. Check Settings.")
        except RateLimitError:
            raise RuntimeError("OpenAI rate limit hit, try again in a moment")

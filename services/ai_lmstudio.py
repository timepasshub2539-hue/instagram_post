import os
import json
from openai import OpenAI
from services.prompts import build_prompt


def generate_with_lmstudio(mood: str, user_context: str, model: str = "local-model", base_url: str = None) -> dict:
    if base_url is None:
        base_url = os.getenv("LMSTUDIO_URL", "http://localhost:1234/v1")

    # LM Studio accepts any string as the API key
    client = OpenAI(base_url=base_url, api_key="lm-studio")
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
        except Exception as e:
            err = str(e).lower()
            if any(w in err for w in ("connection", "refused", "connect", "timeout", "unreachable")):
                raise RuntimeError("LM Studio not found. Open LM Studio, load a model, and start the local server.")
            raise

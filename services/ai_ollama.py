import json
import random
import ollama
from services.prompts import build_prompt


def generate_with_ollama(mood: str, user_context: str, model: str = "llama3") -> dict:
    prompt_text = build_prompt(mood, user_context)

    for attempt in range(2):
        try:
            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": prompt_text}],
                options={"temperature": 0.9, "seed": random.randint(1, 999999)},
            )
            # SDK >= 0.3 returns an object; older versions return a dict
            if hasattr(response, "message"):
                raw = response.message.content
            else:
                raw = response["message"]["content"]

            raw = raw.strip()
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
            if any(w in err for w in ("connection", "refused", "connect", "unavailable", "timeout", "httpx")):
                raise RuntimeError("Local AI not found. Start Ollama on your computer or switch to Online mode")
            raise

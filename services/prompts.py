import random

_ANGLES = [
    "Focus on the quiet, private feeling no one talks about.",
    "Focus on a specific moment — a late night, a look, a message left on read.",
    "Focus on the contradiction — wanting something and being scared of it at the same time.",
    "Focus on the body feeling — the chest tightness, the stomach drop, the restless legs.",
    "Focus on what you tell yourself vs what you actually feel.",
    "Focus on the version of you that pretends everything is fine.",
    "Focus on a turning point — the moment something shifted.",
    "Focus on the small everyday things that carry the big feelings.",
    "Focus on the exhaustion of keeping it together every single day.",
    "Focus on what you wish someone would just say to you right now.",
    "Focus on the gap between who you are and who everyone thinks you are.",
    "Focus on the loneliness of being surrounded by people but still feeling invisible.",
]

_STARTERS = [
    "Start the hook with a question.",
    "Start the hook with 'You'.",
    "Start the hook with 'Nobody talks about'.",
    "Start the hook with a short incomplete sentence.",
    "Start the hook with 'It's the'.",
    "Start the hook with 'Some days'.",
    "Start the hook mid-thought, like you're already deep in it.",
]

_TONES = [
    "Write it gentle, like you're talking to yourself in the mirror.",
    "Write it tired — like someone who hasn't slept and has stopped pretending.",
    "Write it with a little dark humour, like laughing through the pain.",
    "Write it urgent, like this thought has been sitting in your chest for weeks.",
    "Write it soft — like a note left on the nightstand.",
]


def build_prompt(mood: str, user_context: str) -> str:
    angle   = random.choice(_ANGLES)
    starter = random.choice(_STARTERS)
    tone    = random.choice(_TONES)
    # Random variation token forces the model out of any cached pattern
    token   = random.randint(10000, 99999)

    return f"""You are a raw, authentic voice for a Gen-Z/millennial Instagram journal page targeting young Indians aged 18-30 dealing with real emotions.
Your writing style is honest, conversational, like a text message from a close friend.
Never preachy. Never generic. Never use words like journey, hustle, grind, manifest.

Creative direction for THIS carousel (variation #{token}):
- Angle: {angle}
- Hook style: {starter}
- Tone: {tone}

Mood: {mood}
User context: {user_context if user_context else "none provided"}

Return ONLY a valid JSON object with exactly these keys:
{{
  "hook": "One powerful sentence under 12 words that stops the scroll. No hashtags.",
  "slide2": "One raw honest thought. 2-3 short sentences. First person.",
  "slide3": "One raw honest thought. 2-3 short sentences. First person.",
  "slide4": "One raw honest thought. 2-3 short sentences. First person.",
  "closer": "A note to self OR a question that makes people comment. Under 15 words.",
  "caption": "Instagram caption. 3-4 lines. Conversational. End with one question. Only 3-5 hashtags.",
  "hashtags": ["list", "of", "8", "hashtags", "without", "the", "hash", "symbol"]
}}

Rules:
- Sound like a real person wrote this at 2am
- Specific emotions, not vague inspiration
- Each slide must feel like a completely different thought from the others
- The hook must make someone think "oh that is exactly me"
- Return raw JSON only, no markdown, no code blocks"""

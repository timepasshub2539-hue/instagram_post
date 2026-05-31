"""
Run this once after installing requirements:
    python setup.py
Downloads required fonts and creates necessary folders.
"""
import os
import json
import requests

# Map filename → Google Fonts family name
FONTS = {
    "DMSans-Regular.ttf": "DM Sans",
    "PlayfairDisplay-Regular.ttf": "Playfair Display",
    "SourceCodePro-Regular.ttf": "Source Code Pro",
    "Poppins-Regular.ttf": "Poppins",
    "Raleway-Regular.ttf": "Raleway",
    "Nunito-Regular.ttf": "Nunito",
}

# Use an old User-Agent so Google Fonts returns TTF format instead of woff2
# Android 2.2 UA → Google Fonts serves TTF format (not EOT/woff2)
_OLD_UA = "Mozilla/5.0 (Linux; Android 2.2; Nexus One) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"


def download_font(family_name: str, dest_path: str) -> None:
    """Download a TTF font from Google Fonts by following the CSS API redirect URL."""
    import re
    css_url = f"https://fonts.googleapis.com/css?family={family_name.replace(' ', '+')}"
    css = requests.get(css_url, headers={"User-Agent": _OLD_UA}, timeout=15)
    css.raise_for_status()
    # Google Fonts now returns a /l/font?kit= redirect URL instead of a direct .ttf link
    match = re.search(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", css.text)
    if not match:
        raise ValueError("Could not find font URL in Google Fonts CSS response")
    font_url = match.group(1)
    # Follow the redirect (allow_redirects=True is the default)
    font_data = requests.get(font_url, headers={"User-Agent": _OLD_UA}, timeout=30)
    font_data.raise_for_status()
    with open(dest_path, "wb") as f:
        f.write(font_data.content)


os.makedirs("assets/fonts", exist_ok=True)
os.makedirs("data/drafts", exist_ok=True)

for filename, family in FONTS.items():
    path = f"assets/fonts/{filename}"
    if not os.path.exists(path):
        print(f"Downloading {filename} ({family})...")
        try:
            download_font(family, path)
            print(f"  Saved to {path}")
        except Exception as e:
            print(f"  WARNING: Could not download {filename}: {e}")
            print(f"  App will fall back to default font for this typeface.")
    else:
        print(f"  {filename} already exists, skipping")

settings_path = "data/settings.json"
if not os.path.exists(settings_path):
    with open(settings_path, "w") as f:
        json.dump({
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
            "onboarding_complete": False
        }, f, indent=2)
    print("Created data/settings.json")
else:
    print("  data/settings.json already exists, skipping")

print("\nSetup complete! Run: python main.py")

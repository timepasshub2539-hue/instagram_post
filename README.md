# JournalDrop

AI-powered Instagram carousel journal engine. Pick a mood, Claude writes 5 authentic slides, you edit and export as PNG.

**Stack:** Python + FastAPI + Pillow + Anthropic Claude / Ollama

---

## Quick Start

```bash
# 1. Clone the project
git clone https://github.com/yourname/journaldrop
cd journaldrop

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
cp .env.example .env
# Open .env and add your ANTHROPIC_API_KEY

# 5. Download fonts and create folders
python setup.py

# 6. Start the app
python main.py

# 7. Open in browser
# Desktop: http://localhost:8000
# Phone (same WiFi): http://YOUR_COMPUTER_IP:8000
```

---

## Local AI (no API key needed)

```bash
# Install Ollama from https://ollama.ai
ollama pull llama3

# Ollama runs on http://localhost:11434 automatically
# In JournalDrop Settings → switch AI Mode to "Local"
```

---

## Features

- **10 moods** — Overthinking, Heartbreak, Career Pressure, and more
- **5-slide carousels** — Hook → 3 raw thoughts → Closer
- **Dual AI modes** — Claude API (online) or Ollama (offline)
- **Pillow image renderer** — 1080×1080 Instagram-ready PNGs
- **ZIP export** — Download all 5 slides in one click
- **Design panel** — Dark/light theme, 3 fonts, font size, text alignment
- **Drafts** — Auto-saved, max 50, editable
- **Mobile-first** — Works on phone via browser, no app install needed

---

## Project Structure

```
main.py              — Entry point
routers/             — FastAPI route handlers
services/            — AI logic + image renderer
models/schemas.py    — Pydantic models
static/              — Frontend (HTML + CSS + JS)
data/                — Drafts + settings (auto-created)
assets/fonts/        — TTF fonts (downloaded by setup.py)
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/generate` | Generate carousel with AI |
| POST | `/api/render` | Render slides to base64 PNG |
| GET | `/api/export/{id}` | Download ZIP of 5 PNGs |
| GET | `/api/drafts` | List all drafts |
| GET | `/api/drafts/{id}` | Get one draft |
| POST | `/api/drafts/{id}` | Save/update draft |
| DELETE | `/api/drafts/{id}` | Delete draft |
| GET | `/api/settings` | Get settings |
| POST | `/api/settings` | Update settings |

Interactive API docs: `http://localhost:8000/docs`

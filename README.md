# JournalDrop

AI-powered Instagram carousel journal engine. Pick a mood, Claude writes 5 authentic slides, you edit and export as PNG.

**Stack:** Python + FastAPI + Pillow + Anthropic Claude / OpenAI / Mistral / Ollama / LM Studio

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

# 4. Download fonts and create folders
python setup.py

# 5. Start the app
python main.py

# 6. Open in browser
# Desktop: http://localhost:8000
# Phone (same WiFi): http://YOUR_COMPUTER_IP:8000
```

> **API keys** can be added directly in the app — go to **Settings → API Keys** and paste your key. No `.env` file required.

---

## API Keys

You have two options — use whichever is easier:

**Option A — In-app (recommended)**
Open `http://localhost:8000/settings`, scroll to **API Keys**, paste your key, and hit **Save Settings**. Keys are stored locally in `data/settings.json`.

**Option B — `.env` file**
```bash
cp .env.example .env
# add ANTHROPIC_API_KEY, OPENAI_API_KEY, or MISTRAL_API_KEY
```
Environment variables take priority over keys saved in Settings.

---

## AI Backends

| Mode | Requires | Notes |
|------|----------|-------|
| Claude (Anthropic) | API key | Default, highest quality |
| OpenAI (GPT) | API key | GPT-4o-mini by default |
| Mistral | API key | mistral-small-latest by default |
| Ollama | Local install | Free, runs offline |
| LM Studio | Local install | Free, runs offline |

**Ollama setup:**
```bash
# Install from https://ollama.ai
ollama pull llama3
# Then in Settings → AI Mode → Local
```

---

## Features

- **10 moods** — Overthinking, Heartbreak, Career Pressure, and more
- **5-slide carousels** — Hook → 3 raw thoughts → Closer
- **5 AI backends** — Claude, OpenAI, Mistral, Ollama, LM Studio
- **In-app API key management** — paste keys in Settings, no `.env` needed
- **Pillow image renderer** — 1080×1080 Instagram-ready PNGs
- **ZIP export** — Download all 5 slides in one click
- **Design panel** — Dark/light theme, 6 fonts, font size, text alignment
- **Drafts** — Auto-saved, max 50, editable
- **Mobile-first** — Works on phone via browser, no app install needed

---

## Project Structure

```
main.py              — Entry point
routers/             — FastAPI route handlers
services/            — AI logic + image renderer
  api_keys.py        — Key resolution (env var → settings fallback)
models/schemas.py    — Pydantic models
static/              — Frontend (HTML + CSS + JS)
data/                — Drafts + settings (auto-created, gitignored)
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
| GET | `/api/settings` | Get settings + AI availability flags |
| POST | `/api/settings` | Update settings (including API keys) |

Interactive API docs: `http://localhost:8000/docs`

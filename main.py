from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from routers import generate, render, export, drafts, settings
import uvicorn
import os

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="JournalDrop")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(generate.router, prefix="/api")
app.include_router(render.router, prefix="/api")
app.include_router(export.router, prefix="/api")
app.include_router(drafts.router, prefix="/api")
app.include_router(settings.router, prefix="/api")


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/preview")
def preview():
    return FileResponse("static/preview.html")


@app.get("/drafts")
def drafts_page():
    return FileResponse("static/drafts.html")


@app.get("/schedule")
def schedule_page():
    return FileResponse("static/schedule.html")


@app.get("/settings")
def settings_page():
    return FileResponse("static/settings.html")


if __name__ == "__main__":
    # Ensure required directories exist before starting
    os.makedirs("data/drafts", exist_ok=True)
    os.makedirs("assets/fonts", exist_ok=True)
    if not os.path.exists("data/settings.json"):
        import json
        with open("data/settings.json", "w") as f:
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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

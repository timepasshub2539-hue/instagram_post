import json
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from services.image_renderer import render_all_slides, images_to_zip

router = APIRouter()
DRAFTS_DIR = "data/drafts"


def _load_settings() -> dict:
    try:
        with open("data/settings.json") as f:
            return json.load(f)
    except Exception:
        return {}


@router.get("/export/{carousel_id}")
def export_carousel(carousel_id: str):
    draft_path = os.path.join(DRAFTS_DIR, f"{carousel_id}.json")
    if not os.path.exists(draft_path):
        raise HTTPException(status_code=404, detail="Carousel not found")

    with open(draft_path) as f:
        carousel_data = json.load(f)

    settings = _load_settings()

    if carousel_data.get("design"):
        design = carousel_data["design"]
    else:
        theme = settings.get("default_theme", "dark")
        if theme == "light":
            design = {
                "theme": "light",
                "font": settings.get("default_font", "DMSans"),
                "font_size_body": 48,
                "font_size_large": 72,
                "background_color": "#fafafa",
                "text_color": "#1a1a1a",
                "accent_color": "#7c3aed",
                "text_align": "left",
                "handle": settings.get("instagram_handle", ""),
            }
        else:
            design = {
                "theme": "dark",
                "font": settings.get("default_font", "DMSans"),
                "font_size_body": 48,
                "font_size_large": 72,
                "background_color": "#0d0d0d",
                "text_color": "#f5f5f5",
                "accent_color": "#a78bfa",
                "text_align": "left",
                "handle": settings.get("instagram_handle", ""),
            }

    handle = design.get("handle", "")
    images = render_all_slides(carousel_data, design, handle)
    zip_bytes = images_to_zip(images, carousel_id)

    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="carousel-{carousel_id[:8]}.zip"'}
    )

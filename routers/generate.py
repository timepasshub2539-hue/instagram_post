import os
import json
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException
from models.schemas import GenerateRequest, GenerateResponse, CarouselData
from services.ai_router import generate_carousel

router = APIRouter()
DRAFTS_DIR = "data/drafts"
MAX_DRAFTS = 50


def _enforce_draft_cap():
    """Delete oldest drafts when over limit."""
    files = []
    for fname in os.listdir(DRAFTS_DIR):
        if fname.endswith(".json"):
            fpath = os.path.join(DRAFTS_DIR, fname)
            try:
                with open(fpath) as f:
                    data = json.load(f)
                files.append((data.get("created_at", ""), fpath))
            except Exception:
                pass
    if len(files) >= MAX_DRAFTS:
        files.sort(key=lambda x: x[0])
        for _, fpath in files[:len(files) - MAX_DRAFTS + 1]:
            os.remove(fpath)


@router.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    try:
        result = generate_carousel(request.mood, request.user_context, request.ai_mode)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

    carousel_id = str(uuid.uuid4())
    draft = {
        "id": carousel_id,
        "created_at": datetime.utcnow().isoformat(),
        "mood": request.mood,
        "user_context": request.user_context,
        "hook": result.get("hook", ""),
        "slide2": result.get("slide2", ""),
        "slide3": result.get("slide3", ""),
        "slide4": result.get("slide4", ""),
        "closer": result.get("closer", ""),
        "caption": result.get("caption", ""),
        "hashtags": result.get("hashtags", []),
        "design": None,
        "scheduled_for": None,
        "status": "draft"
    }

    os.makedirs(DRAFTS_DIR, exist_ok=True)
    _enforce_draft_cap()
    with open(os.path.join(DRAFTS_DIR, f"{carousel_id}.json"), "w") as f:
        json.dump(draft, f, indent=2)

    return GenerateResponse(
        success=True,
        carousel=CarouselData(
            id=carousel_id,
            mood=draft["mood"],
            hook=draft["hook"],
            slide2=draft["slide2"],
            slide3=draft["slide3"],
            slide4=draft["slide4"],
            closer=draft["closer"],
            caption=draft["caption"],
            hashtags=draft["hashtags"],
        )
    )

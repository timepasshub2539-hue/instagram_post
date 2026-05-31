import json
import os
from fastapi import APIRouter, HTTPException
from models.schemas import DraftModel

router = APIRouter()
DRAFTS_DIR = "data/drafts"


def _list_drafts_sorted() -> list:
    drafts = []
    for fname in os.listdir(DRAFTS_DIR):
        if fname.endswith(".json"):
            try:
                with open(os.path.join(DRAFTS_DIR, fname)) as f:
                    drafts.append(json.load(f))
            except Exception:
                pass
    drafts.sort(key=lambda d: d.get("created_at", ""), reverse=True)
    return drafts


@router.get("/drafts")
def list_drafts():
    os.makedirs(DRAFTS_DIR, exist_ok=True)
    return {"drafts": _list_drafts_sorted()}


@router.get("/drafts/{draft_id}")
def get_draft(draft_id: str):
    path = os.path.join(DRAFTS_DIR, f"{draft_id}.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Draft not found")
    with open(path) as f:
        return json.load(f)


@router.post("/drafts/{draft_id}")
def save_draft(draft_id: str, draft: dict):
    os.makedirs(DRAFTS_DIR, exist_ok=True)
    path = os.path.join(DRAFTS_DIR, f"{draft_id}.json")
    # Preserve id in case body omits it
    draft["id"] = draft_id
    with open(path, "w") as f:
        json.dump(draft, f, indent=2)
    return {"success": True}


@router.delete("/drafts/{draft_id}")
def delete_draft(draft_id: str):
    path = os.path.join(DRAFTS_DIR, f"{draft_id}.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Draft not found")
    os.remove(path)
    return {"success": True}

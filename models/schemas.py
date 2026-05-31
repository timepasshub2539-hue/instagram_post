from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class GenerateRequest(BaseModel):
    mood: str
    user_context: str = ""
    ai_mode: str = "online"  # "online" or "local"


class CarouselData(BaseModel):
    id: str
    mood: str
    hook: str
    slide2: str
    slide3: str
    slide4: str
    closer: str
    caption: str
    hashtags: List[str]


class GenerateResponse(BaseModel):
    success: bool
    carousel: CarouselData


class DesignConfig(BaseModel):
    theme: str = "dark"
    font: str = "DMSans"
    font_size_body: int = 48
    font_size_large: int = 72
    background_color: str = "#0d0d0d"
    text_color: str = "#f5f5f5"
    accent_color: str = "#a78bfa"
    text_align: str = "left"
    handle: str = ""


class RenderRequest(BaseModel):
    carousel_id: str
    design: Optional[DesignConfig] = None


class RenderResponse(BaseModel):
    success: bool
    images: List[str]  # base64-encoded PNG strings


class DraftModel(BaseModel):
    id: str
    created_at: str
    mood: str
    user_context: str = ""
    hook: str
    slide2: str
    slide3: str
    slide4: str
    closer: str
    caption: str
    hashtags: List[str] = []
    design: Optional[dict] = None
    scheduled_for: Optional[str] = None
    status: str = "draft"


class SettingsModel(BaseModel):
    ai_mode: str = "online"
    ollama_model: str = "llama3"
    default_theme: str = "dark"
    default_font: str = "DMSans"
    instagram_handle: str = ""
    posting_time_1: str = "06:00"
    posting_time_2: str = "21:00"
    niche: str = ""
    onboarding_complete: bool = False

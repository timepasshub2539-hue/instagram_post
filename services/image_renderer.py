import io
import os
from PIL import Image, ImageDraw, ImageFont

CANVAS_SIZE = (1080, 1080)
FONT_DIR = "assets/fonts"

FONT_FILES = {
    "DMSans": "DMSans-Regular.ttf",
    "PlayfairDisplay": "PlayfairDisplay-Regular.ttf",
    "SourceCodePro": "SourceCodePro-Regular.ttf",
    "Poppins": "Poppins-Regular.ttf",
    "Raleway": "Raleway-Regular.ttf",
    "Nunito": "Nunito-Regular.ttf",
}

DARK_THEME = {
    "background_color": "#0d0d0d",
    "text_color": "#f5f5f5",
    "accent_color": "#a78bfa",
}

LIGHT_THEME = {
    "background_color": "#fafafa",
    "text_color": "#1a1a1a",
    "accent_color": "#7c3aed",
}


def _hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _load_font(font_name: str, size: int) -> ImageFont.FreeTypeFont:
    filename = FONT_FILES.get(font_name, "DMSans-Regular.ttf")
    path = os.path.join(FONT_DIR, filename)
    try:
        return ImageFont.truetype(path, size=size)
    except Exception:
        print(f"WARNING: Font {path} not found, using default font")
        try:
            return ImageFont.load_default(size=size)
        except Exception:
            return ImageFont.load_default()


def _compute_lines(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list:
    """Break text into word-wrapped lines that fit within max_width pixels."""
    words = text.split()
    lines = []
    current = []
    for word in words:
        test = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines or [""]


def _measure_lines_height(draw: ImageDraw.ImageDraw, lines: list, font, line_spacing: int = 16) -> int:
    """Return total pixel height of a list of lines."""
    total = 0
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        total += bbox[3] - bbox[1]
        if i < len(lines) - 1:
            total += line_spacing
    return total


def draw_wrapped_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font,
    color: tuple,
    x: int,
    y: int,
    max_width: int,
    line_spacing: int = 16,
    align: str = "left",
) -> int:
    """Draw word-wrapped text starting at (x, y). Returns y after last line."""
    lines = _compute_lines(draw, text, font, max_width)
    current_y = y
    for line in lines:
        if align == "center":
            bbox = draw.textbbox((0, 0), line, font=font)
            draw_x = x + (max_width - (bbox[2] - bbox[0])) // 2
        else:
            draw_x = x
        draw.text((draw_x, current_y), line, font=font, fill=color)
        bbox = draw.textbbox((0, 0), line, font=font)
        current_y += (bbox[3] - bbox[1]) + line_spacing
    return current_y


def render_slide(
    text: str,
    slide_number: int,
    total_slides: int,
    design: dict,
    handle: str,
) -> Image.Image:
    bg_color     = _hex_to_rgb(design.get("background_color", DARK_THEME["background_color"]))
    text_color   = _hex_to_rgb(design.get("text_color",       DARK_THEME["text_color"]))
    accent_color = _hex_to_rgb(design.get("accent_color",     DARK_THEME["accent_color"]))
    font_name    = design.get("font", "DMSans")
    font_size_body  = design.get("font_size_body",  48)
    font_size_large = design.get("font_size_large", 72)
    text_align   = design.get("text_align", "left")

    img  = Image.new("RGB", CANVAS_SIZE, color=bg_color)
    draw = ImageDraw.Draw(img)

    # Subtle top accent bar
    draw.rectangle([(80, 60), (200, 68)], fill=accent_color)

    font_main  = _load_font(font_name, font_size_large if slide_number == 1 else font_size_body)
    font_small = _load_font(font_name, 28)

    # Vertically center text in the safe zone (100 → 940)
    SAFE_TOP    = 100
    SAFE_BOTTOM = 940
    MARGIN_X    = 80
    MAX_WIDTH   = CANVAS_SIZE[0] - MARGIN_X * 2   # 920 px

    lines       = _compute_lines(draw, text, font_main, MAX_WIDTH)
    line_spacing = 20
    text_height = _measure_lines_height(draw, lines, font_main, line_spacing)
    available   = SAFE_BOTTOM - SAFE_TOP
    y_start     = SAFE_TOP + max(0, (available - text_height) // 2)

    draw_wrapped_text(
        draw, text, font_main, text_color,
        x=MARGIN_X, y=y_start, max_width=MAX_WIDTH,
        line_spacing=line_spacing, align=text_align,
    )

    # Slide counter — bottom right
    draw.text((980, 1030), f"{slide_number}/{total_slides}",
              font=font_small, fill=accent_color, anchor="rb")

    # Instagram handle on slide 1 — bottom center
    if slide_number == 1 and handle:
        draw.text((540, 1040), f"@{handle}",
                  font=font_small, fill=accent_color, anchor="mb")

    return img


def render_all_slides(carousel_data: dict, design: dict, handle: str) -> list:
    slides_text = [
        carousel_data.get("hook",   ""),
        carousel_data.get("slide2", ""),
        carousel_data.get("slide3", ""),
        carousel_data.get("slide4", ""),
        carousel_data.get("closer", ""),
    ]
    return [render_slide(text, i + 1, len(slides_text), design, handle)
            for i, text in enumerate(slides_text)]


def images_to_base64(images: list) -> list:
    import base64
    result = []
    for img in images:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        result.append(base64.b64encode(buf.getvalue()).decode("utf-8"))
    return result


def images_to_zip(images: list, carousel_id: str) -> bytes:
    import zipfile
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, img in enumerate(images, 1):
            img_buffer = io.BytesIO()
            img.save(img_buffer, format="PNG")
            zf.writestr(f"slide-{i}.png", img_buffer.getvalue())
    return zip_buffer.getvalue()

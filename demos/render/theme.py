"""Shared theme: colours and fonts for AgenticQ demo GIFs.

All demos render at a fixed scale and reuse this palette so the three
walkthroughs (CLI, Web, VS Code) feel like one product.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

FONTS_DIR = Path("C:/Windows/Fonts")

# ---------------------------------------------------------------------------
# Palette — GitHub "dark dimmed" / VS Code dark, kept consistent across demos.
# ---------------------------------------------------------------------------
BG = (13, 17, 23)            # terminal / editor background
PANEL = (22, 27, 34)         # cards, side panels
PANEL_HI = (28, 33, 40)      # hovered / active rows
BORDER = (48, 54, 61)        # hairlines
TITLEBAR = (32, 37, 43)      # window chrome strip

FG = (201, 209, 217)         # primary text
FG_BRIGHT = (240, 246, 252)  # headings
DIM = (139, 148, 158)        # secondary text
FAINT = (90, 99, 108)        # captions

GREEN = (86, 211, 100)
CYAN = (121, 192, 255)
TEAL = (57, 197, 207)
YELLOW = (227, 179, 65)
RED = (248, 81, 73)
PURPLE = (188, 140, 255)
ORANGE = (240, 153, 86)
PROMPT = (57, 211, 131)      # shell prompt glyph

# Traffic-light dots for window chrome
DOT_RED = (255, 95, 86)
DOT_AMBER = (255, 189, 46)
DOT_GREEN = (39, 201, 63)

# VS Code activity-bar / accent
VSC_BLUE = (0, 122, 204)
VSC_BAR = (51, 51, 51)
VSC_SIDE = (37, 37, 38)
VSC_EDITOR = (30, 30, 30)

# Scale: render large, GitHub downscales crisply.
SCALE = 2


def _candidates(*names: str) -> str:
    for n in names:
        p = FONTS_DIR / n
        if p.exists():
            return str(p)
    # Fallback to the first; PIL will raise a clear error if truly missing.
    return str(FONTS_DIR / names[0])


MONO_PATH = _candidates("consola.ttf")
MONO_BOLD_PATH = _candidates("consolab.ttf", "consola.ttf")
UI_PATH = _candidates("segoeui.ttf", "arial.ttf")
UI_BOLD_PATH = _candidates("segoeuib.ttf", "arialbd.ttf", "segoeui.ttf")
UI_SEMI_PATH = _candidates("seguisb.ttf", "segoeuib.ttf", "segoeui.ttf")
EMOJI_PATH = _candidates("seguiemj.ttf")


@lru_cache(maxsize=128)
def mono(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(MONO_PATH, size * SCALE)


@lru_cache(maxsize=128)
def mono_bold(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(MONO_BOLD_PATH, size * SCALE)


@lru_cache(maxsize=128)
def ui(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(UI_PATH, size * SCALE)


@lru_cache(maxsize=128)
def ui_bold(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(UI_BOLD_PATH, size * SCALE)


@lru_cache(maxsize=128)
def ui_semi(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(UI_SEMI_PATH, size * SCALE)


@lru_cache(maxsize=128)
def emoji(size: int) -> ImageFont.FreeTypeFont:
    # Segoe UI Emoji renders only at specific sizes well; 28-ish is the sweet
    # spot, but truetype scales it. embedded_color=True is required at draw.
    return ImageFont.truetype(EMOJI_PATH, size * SCALE)


def px(n: int) -> int:
    """Scale a logical pixel value to the render resolution."""
    return n * SCALE

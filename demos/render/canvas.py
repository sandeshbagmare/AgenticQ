"""Canvas primitives for AgenticQ demo GIFs.

A thin wrapper over PIL that knows how to draw window chrome, rounded panels,
mixed text/emoji runs, and assemble a sequence of "scenes" (each held for a
number of frames) into a smoothly paced, looping GIF.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw

from . import theme as T


class Canvas:
    """A single frame being drawn. Coordinates are in *logical* pixels;
    everything is multiplied by T.SCALE under the hood."""

    def __init__(self, w: int, h: int, bg=T.BG):
        self.w, self.h = w, h
        self.img = Image.new("RGB", (T.px(w), T.px(h)), bg)
        self.d = ImageDraw.Draw(self.img)

    # -- shapes -----------------------------------------------------------
    def rect(self, x, y, w, h, fill=None, outline=None, width=1, radius=0):
        box = [T.px(x), T.px(y), T.px(x + w), T.px(y + h)]
        if radius:
            self.d.rounded_rectangle(box, radius=T.px(radius), fill=fill,
                                     outline=outline, width=T.px(width) if outline else 1)
        else:
            self.d.rectangle(box, fill=fill, outline=outline,
                             width=T.px(width) if outline else 1)

    def line(self, x1, y1, x2, y2, fill=T.BORDER, width=1):
        self.d.line([T.px(x1), T.px(y1), T.px(x2), T.px(y2)], fill=fill, width=T.px(width))

    def dot(self, cx, cy, r, fill):
        self.d.ellipse([T.px(cx - r), T.px(cy - r), T.px(cx + r), T.px(cy + r)], fill=fill)

    # -- text -------------------------------------------------------------
    def text(self, x, y, s, font, fill=T.FG, anchor="la"):
        self.d.text((T.px(x), T.px(y)), s, font=font, fill=fill, anchor=anchor)

    def emoji(self, x, y, glyph, size, anchor="la"):
        self.d.text((T.px(x), T.px(y)), glyph, font=T.emoji(size),
                    embedded_color=True, anchor=anchor)

    def text_w(self, s, font) -> float:
        """Width of a string in logical pixels."""
        return self.d.textlength(s, font=font) / T.SCALE

    # -- window chrome ----------------------------------------------------
    def titlebar(self, title, kind="terminal"):
        """Draw a 28px window title strip with traffic-light dots."""
        bar_h = 30
        self.rect(0, 0, self.w, bar_h, fill=T.TITLEBAR)
        self.line(0, bar_h, self.w, bar_h, fill=T.BORDER, width=1)
        for i, c in enumerate((T.DOT_RED, T.DOT_AMBER, T.DOT_GREEN)):
            self.dot(20 + i * 18, bar_h // 2, 6, c)
        self.text(self.w / 2, bar_h / 2, title, T.ui(11), fill=T.DIM, anchor="mm")
        return bar_h


@dataclass
class Movie:
    """Collects scenes and renders a looping GIF.

    Each scene is (draw_fn, hold_frames). Frames are held by repeating the same
    PIL image reference, which keeps the GIF tiny (GIF dedupes identical frames
    poorly, but disposal=1 + identical bytes still compresses well enough)."""

    w: int
    h: int
    fps: int = 12
    frames: list = field(default_factory=list)

    def scene(self, draw_fn: Callable[[Canvas], None], hold: float = 1.0):
        """Render one scene held for `hold` seconds."""
        c = Canvas(self.w, self.h)
        draw_fn(c)
        n = max(1, int(round(hold * self.fps)))
        for _ in range(n):
            self.frames.append(c.img)

    def typing(self, base_draw, prompt_xy, text, font, fill, hold_end=0.8,
               cps: int = 28, fill_prompt=None):
        """Animate a string being typed at prompt_xy, on top of base_draw."""
        x, y = prompt_xy
        steps = max(1, len(text))
        per = max(1, int(round(self.fps / max(1, cps) * len(text))))
        # produce ~ len(text) incremental frames, then hold
        shown = ""
        for i in range(1, len(text) + 1):
            shown = text[:i]
            c = Canvas(self.w, self.h)
            base_draw(c)
            c.text(x, y, shown, font, fill=fill)
            # blinking cursor
            cur_x = x + c.text_w(shown, font)
            c.rect(cur_x + 1, y, 8, 17, fill=fill)
            self.frames.append(c.img)
        # hold final
        c = Canvas(self.w, self.h)
        base_draw(c)
        c.text(x, y, text, font, fill=fill)
        for _ in range(max(1, int(round(hold_end * self.fps)))):
            self.frames.append(c.img)

    def save(self, path: str | Path, end_hold: float = 1.6):
        if not self.frames:
            raise RuntimeError("no frames to save")
        # hold last frame a beat before the loop restarts
        last = self.frames[-1]
        for _ in range(int(round(end_hold * self.fps))):
            self.frames.append(last)
        duration = int(1000 / self.fps)
        # Downscale to half (the SCALE) with LANCZOS for crisp output.
        out_w, out_h = self.frames[0].width // T.SCALE, self.frames[0].height // T.SCALE
        scaled = [f.resize((out_w, out_h), Image.LANCZOS) for f in self.frames]
        # Palettize for smaller files; ADAPTIVE keeps the dark theme clean.
        scaled = [f.convert("P", palette=Image.ADAPTIVE, colors=256) for f in scaled]
        scaled[0].save(
            path, save_all=True, append_images=scaled[1:],
            duration=duration, loop=0, optimize=True, disposal=2,
        )
        return Path(path)

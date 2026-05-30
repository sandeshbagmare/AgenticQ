"""Demo 2 — Web Interface walkthrough (animated GIF).

Renders a browser-like interface showing the AgenticQ web dashboard:
domain explorer, plugin browser, and recommendations tab.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from render.canvas import Movie, Canvas  # noqa: E402
from render import theme as T  # noqa: E402

W, H = 1000, 600


def browser_chrome(c: Canvas, url="localhost:8080"):
    """Draw browser window chrome."""
    # Title bar
    c.rect(0, 0, W, 30, fill=T.TITLEBAR)
    c.line(0, 30, W, 30, fill=T.BORDER)
    for i, col in enumerate((T.DOT_RED, T.DOT_AMBER, T.DOT_GREEN)):
        c.dot(20 + i * 18, 15, 6, col)
    c.text(W / 2, 15, "AgenticQ Dashboard — Chromium", T.ui(11), fill=T.DIM, anchor="mm")

    # Address bar
    c.rect(60, 40, W - 120, 32, fill=T.PANEL, outline=T.BORDER, radius=16)
    c.text(80, 56, url, T.mono(11), fill=T.DIM, anchor="lm")

    return 72  # content_y


def tabs(c: Canvas, y, active_idx=0):
    """Draw navigation tabs."""
    tab_names = ["Domain Explorer", "Plugin Browser", "Recommendations"]
    x = 40
    for i, name in enumerate(tab_names):
        w = 160
        if i == active_idx:
            c.rect(x, y, w, 36, fill=T.PANEL_HI, outline=T.BORDER, radius=6)
            c.text(x + w / 2, y + 18, name, T.ui_semi(11), fill=T.CYAN, anchor="mm")
        else:
            c.text(x + w / 2, y + 18, name, T.ui(11), fill=T.DIM, anchor="mm")
        x += w + 10
    c.line(40, y + 36, W - 40, y + 36, fill=T.BORDER)
    return y + 46


def build():
    m = Movie(W, H, fps=14)

    # Scene 1: Domain Explorer
    def scene1(c):
        content_y = browser_chrome(c)
        tab_y = tabs(c, content_y, active_idx=0)

        # Domain cards
        domains = [
            ("🐍", "Python Development", "4 plugins"),
            ("⚡", "JavaScript/TypeScript", "3 plugins"),
            ("🔌", "Backend & APIs", "4 plugins"),
            ("☁️", "DevOps & Cloud", "4 plugins"),
        ]
        x, y = 50, tab_y + 20
        for emoji, name, count in domains:
            c.rect(x, y, 220, 80, fill=T.PANEL, outline=T.BORDER, radius=8)
            c.emoji(x + 15, y + 12, emoji, 20)
            c.text(x + 55, y + 20, name, T.ui_bold(12), fill=T.FG_BRIGHT)
            c.text(x + 55, y + 45, count, T.ui(10), fill=T.DIM)
            x += 240
            if x > W - 240:
                x = 50
                y += 100

    m.scene(scene1, hold=1.8)

    # Scene 2: Recommendations tab
    def scene2(c):
        content_y = browser_chrome(c)
        tab_y = tabs(c, content_y, active_idx=2)

        # Input + button
        c.rect(50, tab_y + 20, W - 400, 40, fill=T.PANEL, outline=T.BORDER, radius=6)
        c.text(65, tab_y + 40, "Describe your project or paste requirements...", T.ui(11), fill=T.FAINT, anchor="lm")
        c.rect(W - 330, tab_y + 20, 280, 40, fill=T.CYAN, radius=6)
        c.text(W - 190, tab_y + 40, "Scan & Recommend", T.ui_bold(12), fill=(13, 17, 23), anchor="mm")

        # Recommendation cards
        recs = [
            ("python-development", "30.0", "30,218 tokens", "Matches Python project, fastapi"),
            ("unit-testing", "30.0", "2,862 tokens", "Supports testing workflow"),
            ("backend-development", "30.0", "26,426 tokens", "Relevant for development"),
        ]
        y = tab_y + 80
        for name, score, tokens, reason in recs:
            c.rect(50, y, W - 100, 70, fill=T.PANEL, outline=T.BORDER, radius=6)
            c.text(70, y + 15, name, T.mono_bold(12), fill=T.GREEN)
            c.text(70, y + 38, reason, T.ui(10), fill=T.FG)
            c.text(W - 280, y + 15, f"Score: {score}", T.mono(10), fill=T.CYAN)
            c.text(W - 280, y + 38, tokens, T.mono(10), fill=T.YELLOW)
            # Scaffold button
            c.rect(W - 140, y + 20, 80, 28, fill=T.VSC_BLUE, radius=4)
            c.text(W - 100, y + 34, "Scaffold", T.ui_bold(10), fill=T.FG_BRIGHT, anchor="mm")
            y += 80

    m.scene(scene2, hold=2.5)

    # Scene 3: Success state
    def scene3(c):
        content_y = browser_chrome(c)
        tab_y = tabs(c, content_y, active_idx=2)

        # Success banner
        c.rect(50, tab_y + 20, W - 100, 60, fill=T.PANEL, outline=T.GREEN, radius=6)
        c.emoji(70, tab_y + 32, "✅", 18)
        c.text(110, tab_y + 38, "Successfully scaffolded 3 plugins", T.ui_bold(13), fill=T.GREEN)
        c.text(110, tab_y + 58, "Created 24 files in .claude/plugins/", T.ui(11), fill=T.DIM)

    m.scene(scene3, hold=1.8)

    out = Path(__file__).resolve().parent / "gifs" / "demo2_web.gif"
    m.save(out)
    print("wrote", out)


if __name__ == "__main__":
    build()

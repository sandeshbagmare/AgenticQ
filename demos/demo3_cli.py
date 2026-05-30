"""Demo 3 — CLI walkthrough (animated GIF).

Renders a realistic terminal session showing the AgenticQ CLI: recommend,
search, info, and scaffold. All output text mirrors the real CLI captured
from `python -m agenticq.cli ...` against the bundled example projects.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from render.canvas import Movie  # noqa: E402
from render import theme as T  # noqa: E402

W, H = 860, 540
PROMPT = "PS C:\\my-fastapi-app>"


def prompt_line(c, x, y, cmd, typed=None):
    c.text(x, y, PROMPT, T.mono(13), fill=T.PROMPT)
    pw = c.text_w(PROMPT + " ", T.mono(13))
    c.text(x + pw, y, cmd if typed is None else typed, T.mono(13), fill=T.FG_BRIGHT)
    return x + pw


def header(c, title):
    bar = c.titlebar(title)
    return bar + 14


def build():
    m = Movie(W, H, fps=14)
    LX = 22
    cmd1 = "agenticq recommend"

    # ---- Scene A: intro / typing the recommend command -----------------
    def base_intro(c):
        header(c, "Windows PowerShell — AgenticQ CLI")

    def typed_base(c):
        header(c, "Windows PowerShell — AgenticQ CLI")
        c.text(LX, 44, PROMPT, T.mono(13), fill=T.PROMPT)

    px = LX + m_textw(PROMPT + " ")
    m.scene(lambda c: (typed_base(c)), hold=0.5)
    m.typing(typed_base, (px, 44), cmd1, T.mono(13), T.FG_BRIGHT, hold_end=0.5)

    # ---- Scene B: recommend output -------------------------------------
    def scene_reco(c):
        header(c, "Windows PowerShell — AgenticQ CLI")
        prompt_line(c, LX, 44, cmd1)
        y = 72
        c.text(LX, y, "Scanning project...", T.mono(12), fill=T.CYAN); y += 24
        c.text(LX, y, "Detected:", T.mono_bold(12), fill=T.FG_BRIGHT); y += 20
        for label, val, col in [
            ("  Languages:", "python", T.GREEN),
            ("  Frameworks:", "fastapi", T.GREEN),
            ("  Databases:", "postgresql", T.GREEN),
            ("  Testing:", "pytest, test-directory", T.GREEN),
        ]:
            c.text(LX, y, label, T.mono(12), fill=T.DIM)
            c.text(LX + c.text_w(label + " ", T.mono(12)), y, val, T.mono(12), fill=col)
            y += 18
        y += 6
        c.text(LX, y, "Generating recommendations...", T.mono(12), fill=T.CYAN); y += 26
        _reco_table(c, LX, y)
    m.scene(scene_reco, hold=3.2)

    # ---- Scene C: search ----------------------------------------------
    cmd2 = "agenticq search fastapi"

    def search_base(c):
        header(c, "Windows PowerShell — AgenticQ CLI")
        prompt_line(c, LX, 44, cmd2[:0] or "")
        c.text(LX, 44, PROMPT, T.mono(13), fill=T.PROMPT)
    m.typing(lambda c: (header(c, "Windows PowerShell — AgenticQ CLI"),
                        c.text(LX, 44, PROMPT, T.mono(13), fill=T.PROMPT)),
             (px, 44), cmd2, T.mono(13), T.FG_BRIGHT, hold_end=0.4)

    def scene_search(c):
        header(c, "Windows PowerShell — AgenticQ CLI")
        prompt_line(c, LX, 44, cmd2)
        _search_table(c, LX, 76)
    m.scene(scene_search, hold=3.0)

    # ---- Scene D: scaffold --------------------------------------------
    cmd3 = "agenticq scaffold python-development unit-testing --harness claude-code"
    m.typing(lambda c: (header(c, "Windows PowerShell — AgenticQ CLI"),
                        c.text(LX, 44, PROMPT, T.mono(13), fill=T.PROMPT)),
             (px, 44), cmd3, T.mono(12), T.FG_BRIGHT, hold_end=0.4, cps=42)

    def scene_scaffold(c):
        header(c, "Windows PowerShell — AgenticQ CLI")
        c.text(LX, 44, PROMPT, T.mono(12), fill=T.PROMPT)
        c.text(LX + m_textw(PROMPT + " ", 12), 44, cmd3, T.mono(12), fill=T.FG_BRIGHT)
        y = 74
        c.text(LX, y, "Scaffolding 2 plugins for claude-code...", T.mono(12), fill=T.CYAN); y += 30
        c.emoji(LX, y - 2, "✅", 14)
        c.text(LX + 26, y, "Scaffolded 2 plugins -> .claude/plugins/", T.mono(12), fill=T.GREEN); y += 22
        c.text(LX, y, "Created 18 files", T.mono(12), fill=T.DIM); y += 30
        for path in [".claude/plugins/python-development/",
                     ".claude/plugins/unit-testing/",
                     "  agents/  skills/  commands/"]:
            c.emoji(LX, y - 2, "\U0001F4C1", 13)
            c.text(LX + 24, y, path, T.mono(12), fill=T.CYAN); y += 20
    m.scene(scene_scaffold, hold=3.2)

    out = Path(__file__).resolve().parent / "gifs" / "demo3_cli.gif"
    m.save(out)
    print("wrote", out)


# small helpers needing a throwaway canvas for measuring -------------------
from render.canvas import Canvas  # noqa: E402
_mc = Canvas(10, 10)


def m_textw(s, size=13):
    return _mc.text_w(s, T.mono(size))


def _reco_table(c, x, y):
    cols = [(0, "Plugin", T.GREEN), (250, "Score", T.CYAN),
            (340, "Tokens", T.YELLOW), (440, "Reason", T.FG)]
    rows = [
        ("python-development", "30.0", "30,218", "matches Python project, fastapi"),
        ("unit-testing", "30.0", "2,862", "supports testing workflow"),
        ("tdd-workflows", "30.0", "11,366", "relevant for workflows"),
        ("code-refactoring", "30.0", "2,416", "relevant for utilities"),
        ("data-engineering", "30.0", "17,519", "relevant for data"),
    ]
    w = W - 2 * x
    c.rect(x, y, w, 22 + len(rows) * 20 + 8, fill=T.PANEL, outline=T.BORDER, radius=6)
    c.text(x + 12, y + 6, "Recommended Plugins", T.mono_bold(11), fill=T.PURPLE)
    hy = y + 26
    for dx, label, _ in cols:
        c.text(x + 12 + dx, hy, label, T.mono_bold(11), fill=T.DIM)
    c.line(x + 8, hy + 16, x + w - 8, hy + 16, fill=T.BORDER)
    ry = hy + 22
    for name, score, tok, reason in rows:
        c.text(x + 12, ry, name, T.mono(11), fill=T.GREEN)
        c.text(x + 12 + 250, ry, score, T.mono(11), fill=T.CYAN)
        c.text(x + 12 + 340, ry, tok, T.mono(11), fill=T.YELLOW)
        c.text(x + 12 + 440, ry, reason, T.mono(11), fill=T.FG)
        ry += 20


def _search_table(c, x, y):
    rows = [
        ("agent", "api-scaffolding/api-scaffolding", "Build async APIs with FastAPI"),
        ("skill", "api-scaffolding/fastapi-template", "Production-ready FastAPI projects"),
        ("plugin", "python-development", "Modern Python 3.12+, Django, FastAPI"),
        ("agent", "python-development/fastapi-pro", "High-performance async APIs"),
        ("agent", "python-development/python-pro", "Master Python 3.12+ async"),
    ]
    w = W - 2 * x
    c.rect(x, y, w, 22 + len(rows) * 20 + 8, fill=T.PANEL, outline=T.BORDER, radius=6)
    c.text(x + 12, y + 6, "Search Results for 'fastapi'", T.mono_bold(11), fill=T.PURPLE)
    hy = y + 26
    for dx, label in [(0, "Type"), (80, "Name"), (380, "Description")]:
        c.text(x + 12 + dx, hy, label, T.mono_bold(11), fill=T.DIM)
    c.line(x + 8, hy + 16, x + w - 8, hy + 16, fill=T.BORDER)
    ry = hy + 22
    colors = {"plugin": T.PURPLE, "agent": T.CYAN, "skill": T.TEAL}
    for typ, name, desc in rows:
        c.text(x + 12, ry, typ, T.mono(11), fill=colors[typ])
        c.text(x + 12 + 80, ry, name, T.mono(11), fill=T.GREEN)
        c.text(x + 12 + 380, ry, desc, T.mono(11), fill=T.FG)
        ry += 20


if __name__ == "__main__":
    build()

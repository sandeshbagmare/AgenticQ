"""Demo 1 — VS Code Extension walkthrough (animated GIF).

Renders a VS Code-like interface showing the AgenticQ extension in action:
command palette, recommendations, and scaffolding workflow.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from render.canvas import Movie, Canvas  # noqa: E402
from render import theme as T  # noqa: E402

W, H = 1000, 600


def vscode_chrome(c: Canvas, title="AgenticQ Demo"):
    """Draw VS Code window chrome."""
    # Title bar
    c.rect(0, 0, W, 30, fill=T.TITLEBAR)
    c.line(0, 30, W, 30, fill=T.BORDER)
    for i, col in enumerate((T.DOT_RED, T.DOT_AMBER, T.DOT_GREEN)):
        c.dot(20 + i * 18, 15, 6, col)
    c.text(W / 2, 15, title, T.ui(11), fill=T.DIM, anchor="mm")

    # Activity bar (left)
    c.rect(0, 30, 50, H - 30, fill=T.VSC_BAR)
    c.line(50, 30, 50, H, fill=T.BORDER)

    # Sidebar
    c.rect(50, 30, 250, H - 30, fill=T.VSC_SIDE)
    c.line(300, 30, 300, H, fill=T.BORDER)

    # Editor area
    c.rect(300, 30, W - 300, H - 30, fill=T.VSC_EDITOR)

    return 30, 50, 300  # title_h, sidebar_x, editor_x


def build():
    m = Movie(W, H, fps=14)

    # Scene 1: Command Palette opening
    def scene1(c):
        title_h, sidebar_x, editor_x = vscode_chrome(c, "VS Code — my-fastapi-app")
        # Activity bar icon (AgenticQ)
        c.emoji(15, 60, "🤖", 18)
        # Sidebar header
        c.text(sidebar_x + 15, title_h + 15, "AGENTICQ", T.ui_bold(10), fill=T.FG_BRIGHT)
        c.text(sidebar_x + 15, title_h + 35, "Domains", T.ui(10), fill=T.DIM)
        # Command palette overlay
        pal_y = title_h + 40
        c.rect(W / 2 - 300, pal_y, 600, 50, fill=T.PANEL, outline=T.BORDER, radius=6)
        c.text(W / 2, pal_y + 18, "> AgenticQ: Get Recommendations", T.mono(12), fill=T.CYAN, anchor="mm")

    m.scene(scene1, hold=1.2)

    # Scene 2: Scanning project
    def scene2(c):
        title_h, sidebar_x, editor_x = vscode_chrome(c, "VS Code — my-fastapi-app")
        c.emoji(15, 60, "🤖", 18)
        c.text(sidebar_x + 15, title_h + 15, "AGENTICQ", T.ui_bold(10), fill=T.FG_BRIGHT)
        c.text(sidebar_x + 15, title_h + 35, "Domains", T.ui(10), fill=T.DIM)

        # Notification
        notif_y = H - 80
        c.rect(W - 420, notif_y, 400, 60, fill=T.PANEL, outline=T.BORDER, radius=6)
        c.text(W - 410, notif_y + 12, "AgenticQ", T.ui_bold(11), fill=T.FG_BRIGHT)
        c.text(W - 410, notif_y + 32, "Analyzing project...", T.ui(10), fill=T.DIM)
        # Progress bar
        c.rect(W - 410, notif_y + 45, 380, 6, fill=T.BG, radius=3)
        c.rect(W - 410, notif_y + 45, 200, 6, fill=T.CYAN, radius=3)

    m.scene(scene2, hold=1.0)

    # Scene 3: Recommendations quick pick
    def scene3(c):
        title_h, sidebar_x, editor_x = vscode_chrome(c, "VS Code — my-fastapi-app")
        c.emoji(15, 60, "🤖", 18)
        c.text(sidebar_x + 15, title_h + 15, "AGENTICQ", T.ui_bold(10), fill=T.FG_BRIGHT)
        c.text(sidebar_x + 15, title_h + 35, "Domains", T.ui(10), fill=T.DIM)

        # Quick pick with recommendations
        pick_y = title_h + 40
        c.rect(W / 2 - 300, pick_y, 600, 220, fill=T.PANEL, outline=T.BORDER, radius=6)
        c.text(W / 2 - 285, pick_y + 15, "Select plugins to scaffold", T.ui(11), fill=T.FG_BRIGHT)

        items = [
            ("python-development", "30.0", "30,218", T.GREEN),
            ("unit-testing", "30.0", "2,862", T.GREEN),
            ("backend-development", "30.0", "26,426", T.CYAN),
            ("api-scaffolding", "30.0", "10,315", T.CYAN),
        ]
        y = pick_y + 45
        for name, score, tokens, col in items:
            # Checkbox
            c.rect(W / 2 - 285, y, 14, 14, outline=T.BORDER, radius=2)
            c.rect(W / 2 - 282, y + 3, 8, 8, fill=col, radius=1)
            c.text(W / 2 - 260, y + 7, name, T.mono(10), fill=col, anchor="lm")
            c.text(W / 2 + 100, y + 7, f"Score: {score}", T.mono(9), fill=T.DIM, anchor="lm")
            c.text(W / 2 + 200, y + 7, f"{tokens} tokens", T.mono(9), fill=T.YELLOW, anchor="lm")
            y += 40

    m.scene(scene3, hold=2.5)

    # Scene 4: Scaffolding success
    def scene4(c):
        title_h, sidebar_x, editor_x = vscode_chrome(c, "VS Code — my-fastapi-app")
        c.emoji(15, 60, "🤖", 18)
        c.text(sidebar_x + 15, title_h + 15, "AGENTICQ", T.ui_bold(10), fill=T.FG_BRIGHT)
        c.text(sidebar_x + 15, title_h + 35, "Domains", T.ui(10), fill=T.DIM)

        # Sidebar now shows scaffolded plugins
        y = title_h + 60
        for domain in ["🐍 Python Development", "✅ Testing & QA"]:
            c.text(sidebar_x + 15, y, domain, T.ui(10), fill=T.FG)
            y += 25

        # Success notification
        notif_y = H - 80
        c.rect(W - 420, notif_y, 400, 60, fill=T.PANEL, outline=T.BORDER, radius=6)
        c.emoji(W - 405, notif_y + 10, "✅", 16)
        c.text(W - 375, notif_y + 12, "AgenticQ", T.ui_bold(11), fill=T.FG_BRIGHT)
        c.text(W - 375, notif_y + 32, "Scaffolded 2 plugins → .claude/plugins/", T.ui(10), fill=T.GREEN)

    m.scene(scene4, hold=2.0)

    out = Path(__file__).resolve().parent / "gifs" / "demo1_vscode.gif"
    m.save(out)
    print("wrote", out)


if __name__ == "__main__":
    build()

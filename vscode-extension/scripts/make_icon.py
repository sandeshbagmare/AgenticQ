"""
Generate the AgenticQ marketplace icon (PNG).

Renders a 256x256 PNG: a gradient rounded square with a hexagon "agent
shield" and a hub-and-spoke network (multi-agent orchestration motif),
matching the activity-bar SVG. Supersamples at 4x for clean anti-aliasing.

Run:  python scripts/make_icon.py
Output: ../icon.png  (and a 512px version for the README/social card)
"""
import math
import os
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:  # auto-install Pillow if missing
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
    from PIL import Image, ImageDraw


def lerp(a, b, t):
    return int(a + (b - a) * t)


def vertical_gradient(size, top, bottom):
    """Build a vertical gradient via a 1px column resized to full width."""
    col = Image.new("RGBA", (1, size))
    for y in range(size):
        t = y / (size - 1)
        col.putpixel(
            (0, y),
            (lerp(top[0], bottom[0], t),
             lerp(top[1], bottom[1], t),
             lerp(top[2], bottom[2], t), 255),
        )
    return col.resize((size, size))


def hexagon_points(cx, cy, r):
    """Pointy-top hexagon: vertices every 60 deg starting at the top."""
    pts = []
    for i in range(6):
        ang = math.radians(90 + i * 60)
        pts.append((cx + r * math.cos(ang), cy - r * math.sin(ang)))
    return pts


def render(size, out_path):
    S = size * 4  # supersample
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

    # Gradient background masked by a rounded rectangle.
    grad = vertical_gradient(S, (79, 70, 229), (124, 58, 237))  # #4F46E5 -> #7C3AED
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, S - 1, S - 1], radius=int(S * 0.21), fill=255
    )
    img.paste(grad, (0, 0), mask)

    d = ImageDraw.Draw(img)
    cx = cy = S / 2
    R = S * 0.30
    pts = hexagon_points(cx, cy, R)
    white = (255, 255, 255, 255)
    faint = (255, 255, 255, 150)

    # Spokes from center to each vertex (orchestration graph).
    for p in pts:
        d.line([(cx, cy), p], fill=faint, width=max(2, int(S * 0.010)))

    # Hexagon outline.
    d.line(pts + [pts[0]], fill=white, joint="curve",
           width=max(3, int(S * 0.028)))

    # Vertex nodes.
    nr = S * 0.026
    for p in pts:
        d.ellipse([p[0] - nr, p[1] - nr, p[0] + nr, p[1] + nr], fill=white)

    # Center hub node (slightly larger, with a soft ring).
    hr = S * 0.052
    d.ellipse([cx - hr * 1.7, cy - hr * 1.7, cx + hr * 1.7, cy + hr * 1.7],
              outline=faint, width=max(2, int(S * 0.012)))
    d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=white)

    icon = img.resize((size, size), Image.LANCZOS)
    icon.save(out_path)
    print(f"wrote {out_path} ({size}x{size})")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    ext_root = os.path.dirname(here)
    render(256, os.path.join(ext_root, "icon.png"))
    render(512, os.path.join(ext_root, "icon-512.png"))

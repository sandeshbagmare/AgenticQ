"""Copy demo images from artifacts directory to demos folder."""
import shutil
import os
from pathlib import Path

ARTIFACTS_DIR = Path(os.path.expanduser(r"~\.gemini\antigravity-ide\brain\3d5f7293-52fb-411e-aa9e-b3d7d21c1a1a"))
DEMOS_DIR = Path(__file__).parent

mapping = {
    "demo1_cli_recommend": "demo1_cli_recommend.png",
    "demo2_cli_scaffold": "demo2_cli_scaffold.png",
    "demo3_web_gui": "demo3_web_gui.png",
    "demo4_vscode_extension": "demo4_vscode_extension.png",
    "demo5_cli_search": "demo5_cli_search.png",
}

if ARTIFACTS_DIR.exists():
    for prefix, dest_name in mapping.items():
        # Find the latest file matching the prefix
        matches = sorted(ARTIFACTS_DIR.glob(f"{prefix}*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
        if matches:
            src = matches[0]
            dst = DEMOS_DIR / dest_name
            shutil.copy2(src, dst)
            print(f"  Copied: {src.name} -> {dest_name} ({dst.stat().st_size:,} bytes)")
        else:
            print(f"  MISSING: No file matching '{prefix}*.png'")
else:
    print(f"Artifacts directory not found: {ARTIFACTS_DIR}")
    print("Listing parent...")
    parent = ARTIFACTS_DIR.parent
    if parent.exists():
        for f in parent.iterdir():
            print(f"  {f.name}")

print("\nDone!")

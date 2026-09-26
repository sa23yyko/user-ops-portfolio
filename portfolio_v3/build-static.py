"""Copy the reviewed V3 site into the static hosting directory."""

from pathlib import Path
from shutil import copy2

root = Path(__file__).resolve().parent
output = root / "dist"
(output / "assets").mkdir(parents=True, exist_ok=True)

for name in ("index.html", "styles.css", "app.js"):
    copy2(root / name, output / name)

for name in ("cover-final.png", "STAY_English_PRD.docx"):
    copy2(root / "assets" / name, output / "assets" / name)

print(f"Static site ready: {output}")

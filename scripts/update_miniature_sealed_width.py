#!/usr/bin/env python3
"""
One-off: set the foundation width_B_mm for thin miniature bearings to the
SEALED (ZZ/2RS) width, per web-verified authoritative catalogs
(bearingworks, made-in-china size chart, bearingsinchina, rmobearing).

Only the 68x/69x thin series differ between open and sealed; the standard
60x/62x/63x series share the same width and are left untouched.

Dry-run by default; pass --apply to write.
"""
import json
import sys
from pathlib import Path

# model -> sealed width (mm). Source-corroborated by >=2 catalogs each.
SEALED_WIDTH = {
    "683": 3, "684": 4, "685": 5, "686": 5,
    "687": 5, "688": 5, "689": 5, "693": 4,
}

apply = "--apply" in sys.argv
for model, w in SEALED_WIDTH.items():
    p = Path(f"models/{model}.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    old = data["dimensions"].get("width_B_mm")
    if old == w:
        print(f"{model}: already {w}mm (no change)")
        continue
    print(f"{model}: width_B_mm {old} -> {w}")
    if apply:
        data["dimensions"]["width_B_mm"] = w
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print("APPLIED" if apply else "DRY-RUN (use --apply to write)")

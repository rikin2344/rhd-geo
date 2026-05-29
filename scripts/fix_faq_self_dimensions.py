#!/usr/bin/env python3
"""
FAQ self-dimension fixer
========================

The main consistency fixer treats FAQ text leniently (it can contain
cross-model comparisons), so a few FAQs kept stale self-dimensions
(e.g. 6914 FAQ said 70x95x13 while the verified foundation is 70x100x16,
and miniatures 688/693 kept their pre-sealed widths).

This fixer is deterministic and SELF-REFERENCE GUARDED: inside a FAQ string
it only rewrites a dimension triplet (AxBxC mm) to the model's foundation
triplet when that same FAQ string explicitly names the model number AND the
cited triplet is not already the foundation. This guarantees we never touch a
legitimate cross-model comparison.

Dry-run by default; pass --apply to write.
"""
import json
import glob
import re
import sys
from pathlib import Path

NUM = r'(\d+(?:\.\d+)?)'
TRIP = re.compile(rf'{NUM}\s*[x×]\s*{NUM}\s*[x×]\s*{NUM}\s*mm', re.IGNORECASE)


def fmt(v):
    return str(int(v)) if v == int(v) else ("%g" % v)


def walk(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield path, obj


def set_by_path(root, path, value):
    # path like faqs.foo or a[0].b
    tokens = re.findall(r'[^.\[\]]+|\[\d+\]', path)
    cur = root
    for t in tokens[:-1]:
        if t.startswith('['):
            cur = cur[int(t[1:-1])]
        else:
            cur = cur[t]
    last = tokens[-1]
    if last.startswith('['):
        cur[int(last[1:-1])] = value
    else:
        cur[last] = value


def main():
    apply = "--apply" in sys.argv
    total = 0
    for f in sorted(glob.glob("models/*.json")):
        d = json.loads(Path(f).read_text(encoding="utf-8"))
        m = str(d["model_number"])
        dim = d["dimensions"]
        canon = (dim["bore_diameter_d_mm"], dim["outer_diameter_D_mm"], dim["width_B_mm"])
        canon_str = f"{fmt(canon[0])}x{fmt(canon[1])}x{fmt(canon[2])}mm"
        edits = []
        for path, text in walk(d.get("faqs", {})):
            if m not in text:
                continue  # only self-referential FAQ strings
            trips = TRIP.findall(text)
            if not trips:
                continue
            new = text
            for a, b, c in trips:
                trip = (float(a), float(b), float(c))
                if trip != canon:
                    pat = re.compile(rf'{re.escape(a)}\s*[x×]\s*{re.escape(b)}\s*[x×]\s*{re.escape(c)}\s*mm', re.IGNORECASE)
                    new = pat.sub(canon_str, new)
            if new != text:
                edits.append((f"faqs.{path}", text, new))
                set_by_path(d, f"faqs.{path}", new)
        if edits:
            total += len(edits)
            print(f"\n=== {m} (foundation {canon_str}) ===")
            for fld, old, new in edits:
                bad = TRIP.findall(old)
                print(f"  {fld}: {['×'.join(t) for t in bad]} -> {canon_str}")
            if apply:
                Path(f).write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("\n" + "=" * 50)
    print(f"{'APPLIED' if apply else 'DRY-RUN'} | FAQ dim edits: {total}")


if __name__ == "__main__":
    main()

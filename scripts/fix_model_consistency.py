#!/usr/bin/env python3
"""
Model Consistency Fixer
=======================

Uses each model JSON's verified foundation block (dimensions / load_ratings /
speed_limits) as the single source of truth and rewrites SELF-REFERENTIAL
spec numbers in the derived/prose/schema fields to match it.

Deterministic. No value is invented:
  - kN  -> dynamic_load_Cr_kN or static_load_Cor_kN (by 'static'/'dynamic' context)
  - kg  -> load_capacity_kg (dynamic) or round(Cor*101.97) (static)
  - RPM -> grease_rpm / oil_rpm / recommended_max_rpm (by 'oil'/'recommended' context)
  - dims A×B×C -> d×D×B ; shaft h6 range -> ISO 286 h6 from bore

SAFETY:
  * Only fields known to describe THIS bearing are touched (SAFE_PREFIXES).
  * Any string that mentions ANOTHER known model number or ' vs ' is left
    untouched and reported under 'review' (cross-model comparisons).
  * Dry-run by default. Pass --apply to write files.

Usage:
  python3 scripts/fix_model_consistency.py            # dry-run, all models
  python3 scripts/fix_model_consistency.py 6002       # dry-run, one model
  python3 scripts/fix_model_consistency.py --apply     # write all
  python3 scripts/fix_model_consistency.py 6002 --apply
"""

import json
import re
import sys
from pathlib import Path

KGF_PER_KN = 1000.0 / 9.80665

H6_LOWER_DEV_UM = [
    (0, 3, -6), (3, 6, -8), (6, 10, -9), (10, 18, -11), (18, 30, -13),
    (30, 50, -16), (50, 80, -19), (80, 120, -22), (120, 180, -25), (180, 250, -29),
]

SAFE_PREFIXES = (
    "applications.",
    "seo_metadata.title",
    "seo_metadata.meta_description",
    "seo_metadata.og_data.",
    "seo_metadata.twitter_data.",
    "seo_metadata.schema_markup.name",
    "seo_metadata.schema_markup.description",
    "cross_references.shaft_requirements.",
    "llm_optimization.recommendation_snippets",
    "llm_optimization.decision_criteria",
    "llm_optimization.problem_solution_mapping",
    "llm_optimization.expertise_signals",
)

NUM = r'(\d+(?:,\d{3})*(?:\.\d+)?)'


def to_float(t):
    return float(t.replace(',', ''))


def h6_range(bore):
    lower = 0
    for lo, hi, dev in H6_LOWER_DEV_UM:
        if lo < bore <= hi:
            lower = dev
            break
    return f"h6 ({bore + lower/1000.0:.3f}-{bore:.3f}mm)"


def fmt_kn(v):
    return f"{v:.2f}"


def fmt_mm(v):
    """Format a millimetre value: integers without decimals, else as-is (e.g. 2.5)."""
    if v == int(v):
        return str(int(v))
    return ("%g" % v)


class Canon:
    def __init__(self, data):
        dm, ld, sp = data.get('dimensions', {}), data.get('load_ratings', {}), data.get('speed_limits', {})
        self.model = str(data.get('model_number', '?'))
        self.d, self.D, self.B = dm.get('bore_diameter_d_mm'), dm.get('outer_diameter_D_mm'), dm.get('width_B_mm')
        self.Cr, self.Cor, self.kg = ld.get('dynamic_load_Cr_kN'), ld.get('static_load_Cor_kN'), ld.get('load_capacity_kg')
        self.grease, self.oil, self.rec = sp.get('grease_rpm'), sp.get('oil_rpm'), sp.get('recommended_max_rpm')
        self.cor_kg = round(self.Cor * KGF_PER_KN) if self.Cor else None
        self.h6 = h6_range(self.d) if isinstance(self.d, (int, float)) else None


def fix_string(text, c, other_models):
    """Return (new_text, changes, is_review). is_review=True means skipped (cross-model)."""
    # cross-model guard: another known model number or an explicit comparison
    for tok in re.findall(r'\b\d{3,5}[A-Z]?\d*\b', text):
        if tok in other_models and tok != c.model:
            return text, [], True
    if re.search(r'\bvs\.?\b', text, re.IGNORECASE):
        return text, [], True

    low = text.lower()
    is_static = 'static' in low
    changes = []
    new = text

    # 1) dimension triplet
    def rep_trip(m):
        trip = (to_float(m.group(1)), to_float(m.group(2)), to_float(m.group(3)))
        if trip != (c.d, c.D, c.B):
            changes.append((m.group(0), f"{fmt_mm(c.d)}×{fmt_mm(c.D)}×{fmt_mm(c.B)}mm"))
            return f"{fmt_mm(c.d)}×{fmt_mm(c.D)}×{fmt_mm(c.B)}mm"
        return m.group(0)
    new = re.sub(rf'{NUM}\s*[x×]\s*{NUM}\s*[x×]\s*{NUM}\s*mm', rep_trip, new)

    # 1b) profile pair A×B mm (outer diameter × width)
    def rep_pair(m):
        pair = (to_float(m.group(1)), to_float(m.group(2)))
        if pair != (c.D, c.B):
            changes.append((m.group(0), f"{fmt_mm(c.D)}×{fmt_mm(c.B)}mm"))
            return f"{fmt_mm(c.D)}×{fmt_mm(c.B)}mm"
        return m.group(0)
    new = re.sub(rf'{NUM}\s*[x×]\s*{NUM}\s*mm', rep_pair, new)

    # 1c) standalone bore / width / outer-diameter tokens
    def rep_dim(target, label):
        def _r(m):
            if to_float(m.group(1)) != target:
                changes.append((m.group(0), f"{fmt_mm(target)}mm {label}"))
                return f"{fmt_mm(target)}mm {label}"
            return m.group(0)
        return _r
    new = re.sub(rf'{NUM}\s*mm\s+bore', rep_dim(c.d, 'bore'), new)
    new = re.sub(rf'{NUM}\s*mm\s+width', rep_dim(c.B, 'width'), new)
    new = re.sub(rf'{NUM}\s*mm\s+(?:OD|outer diameter)', rep_dim(c.D, 'OD'), new)

    # 2) h6 range
    def rep_h6(m):
        if c.h6 and m.group(0).replace(' ', '') != c.h6.replace(' ', ''):
            changes.append((m.group(0), c.h6))
            return c.h6
        return m.group(0)
    new = re.sub(r'h6\s*\([\d.]+-[\d.]+mm\)', rep_h6, new)

    # 3) combined "X kN (≈ Y kg)"
    def rep_combo(m):
        kn = c.Cor if is_static else c.Cr
        kg = c.cor_kg if is_static else c.kg
        repl = f"{fmt_kn(kn)}kN (≈{kg}kg)"
        if m.group(0).replace(' ', '') != repl.replace(' ', ''):
            changes.append((m.group(0), repl))
        return repl
    new = re.sub(rf'{NUM}\s*kN\s*\(\s*(?:≈|~|=|about\s*)?\s*{NUM}\s*kg\s*\)', rep_combo, new)

    # 4) remaining standalone kN
    def rep_kn(m):
        val = to_float(m.group(1))
        target = c.Cor if is_static else c.Cr
        if not (abs(val - c.Cr) < 0.005 or (c.Cor and abs(val - c.Cor) < 0.005)):
            changes.append((f"{m.group(1)}kN", f"{fmt_kn(target)}kN"))
            return f"{fmt_kn(target)}kN"
        return m.group(0)
    new = re.sub(rf'{NUM}\s*kN', rep_kn, new)

    # 5) remaining standalone kg
    def rep_kg(m):
        val = to_float(m.group(1))
        target = c.cor_kg if is_static else c.kg
        valid = {c.kg, c.cor_kg}
        if not any(v is not None and abs(val - v) <= 1.5 for v in valid):
            changes.append((f"{m.group(1)}kg", f"{target}kg"))
            return f"{target}kg"
        return m.group(0)
    new = re.sub(rf'{NUM}\s*kg', rep_kg, new)

    # 6) RPM
    def rep_rpm(m):
        val = to_float(m.group(1))
        if 'oil' in low:
            target = c.oil
        elif 'recommend' in low or 'safe operating' in low:
            target = c.rec
        else:
            target = c.grease
        valid = {c.grease, c.oil, c.rec}
        if not any(v is not None and abs(val - v) <= 50 for v in valid):
            changes.append((f"{m.group(1)} RPM", f"{target:,} RPM"))
            return f"{target:,} RPM"
        return m.group(0)
    new = re.sub(rf'{NUM}\s*RPM', rep_rpm, new, flags=re.IGNORECASE)

    return new, changes, False


def fix_node(obj, c, other_models, path, edits, reviews):
    if isinstance(obj, dict):
        return {k: fix_node(v, c, other_models, f"{path}.{k}" if path else k, edits, reviews)
                for k, v in obj.items()}
    if isinstance(obj, list):
        return [fix_node(v, c, other_models, f"{path}[{i}]", edits, reviews)
                for i, v in enumerate(obj)]
    if isinstance(obj, str) and path.startswith(SAFE_PREFIXES):
        new, changes, is_review = fix_string(obj, c, other_models)
        if is_review and (re.search(r'\d+\s*(kN|kg|RPM)', obj, re.I)):
            reviews.append({"field": path, "text": obj.strip()[:160]})
        for old, rep in changes:
            edits.append({"field": path, "from": old, "to": rep})
        return new
    return obj


def main():
    args = [a for a in sys.argv[1:]]
    apply = '--apply' in args
    targets = [a for a in args if not a.startswith('--')]
    only = targets[0] if targets else None

    files = sorted(Path("models").glob("*.json"))
    all_data = {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in files}
    other_models = {str(d.get('model_number')) for d in all_data.values()}

    tot_edits = tot_reviews = files_changed = 0
    for stem, data in all_data.items():
        if only and stem != only:
            continue
        c = Canon(data)
        if c.Cr is None:
            continue
        # also normalise structured shaft fields directly
        edits, reviews = [], []
        new_data = fix_node(data, c, other_models, "", edits, reviews)
        # shaft_requirements structured fields
        sr = new_data.get('cross_references', {}).get('shaft_requirements')
        if isinstance(sr, dict) and c.h6:
            if sr.get('tolerance_grade') != c.h6:
                edits.append({"field": "cross_references.shaft_requirements.tolerance_grade",
                              "from": sr.get('tolerance_grade'), "to": c.h6})
                sr['tolerance_grade'] = c.h6
            nd = f"{c.d:.3f}mm"
            if sr.get('nominal_diameter') != nd:
                edits.append({"field": "cross_references.shaft_requirements.nominal_diameter",
                              "from": sr.get('nominal_diameter'), "to": nd})
                sr['nominal_diameter'] = nd

        if edits:
            files_changed += 1
        tot_edits += len(edits)
        tot_reviews += len(reviews)

        if only or edits or reviews:
            print(f"\n=== {stem} === ({len(edits)} fixes, {len(reviews)} review)")
            for e in edits[:200 if only else 6]:
                print(f"  FIX  {e['field']}: '{e['from']}' -> '{e['to']}'")
            if not only and len(edits) > 6:
                print(f"  ... +{len(edits)-6} more fixes")
            for r in reviews[:50 if only else 3]:
                print(f"  REVIEW {r['field']}: {r['text']}")

        if apply and edits:
            Path(f"models/{stem}.json").write_text(
                json.dumps(new_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("\n" + "=" * 60)
    print(f"{'APPLIED' if apply else 'DRY-RUN'} | files changed: {files_changed} | "
          f"total fixes: {tot_edits} | cross-model strings to review: {tot_reviews}")
    if not apply:
        print("Re-run with --apply to write changes.")


if __name__ == "__main__":
    main()

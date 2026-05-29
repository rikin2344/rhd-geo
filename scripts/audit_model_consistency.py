#!/usr/bin/env python3
"""
Model Consistency Auditor (read-only)
=====================================

Treats each model JSON's foundation block as the single source of truth:

    dimensions      -> bore_diameter_d_mm, outer_diameter_D_mm, width_B_mm, weight_kg
    load_ratings    -> dynamic_load_Cr_kN, static_load_Cor_kN, load_capacity_kg
    speed_limits    -> grease_rpm, oil_rpm, recommended_max_rpm

It then scans the derived / prose / schema fields and reports every number
that disagrees with the foundation block (or its deterministic derivations).

NOTHING is modified. Output is a human report + machine-readable JSON so a
fixer can act on it later.

Severity:
  ERROR  - self-referential spec field contains a value that contradicts the
           foundation block (high confidence, safe to auto-fix).
  REVIEW - free-form / cross-model text where the number may legitimately refer
           to another bearing or a hypothetical scenario (needs judgement).
"""

import json
import re
import sys
from pathlib import Path

KGF_PER_KN = 1000.0 / 9.80665  # 1 kN = 101.9716 kgf

# ISO 286-2 h6 lower deviation (microns); upper deviation = 0
H6_LOWER_DEV_UM = [
    (0, 3, -6), (3, 6, -8), (6, 10, -9), (10, 18, -11), (18, 30, -13),
    (30, 50, -16), (50, 80, -19), (80, 120, -22), (120, 180, -25), (180, 250, -29),
]

NUM = r'(\d+(?:,\d{3})*(?:\.\d+)?)'


def to_float(tok: str) -> float:
    return float(tok.replace(',', ''))


def h6_range(bore_mm: float) -> str:
    lower = 0
    for lo, hi, dev in H6_LOWER_DEV_UM:
        if lo < bore_mm <= hi:
            lower = dev
            break
    low_mm = bore_mm + lower / 1000.0
    return f"h6 ({low_mm:.3f}-{bore_mm:.3f}mm)"


def approx(a: float, b: float, tol: float = 1.5) -> bool:
    return abs(a - b) <= tol


class Canon:
    def __init__(self, data: dict):
        dims = data.get('dimensions', {})
        loads = data.get('load_ratings', {})
        spd = data.get('speed_limits', {})
        self.model = str(data.get('model_number', '?'))
        self.d = dims.get('bore_diameter_d_mm')
        self.D = dims.get('outer_diameter_D_mm')
        self.B = dims.get('width_B_mm')
        self.weight_kg = dims.get('weight_kg')
        self.Cr = loads.get('dynamic_load_Cr_kN')
        self.Cor = loads.get('static_load_Cor_kN')
        self.kg = loads.get('load_capacity_kg')
        self.grease = spd.get('grease_rpm')
        self.oil = spd.get('oil_rpm')
        self.rec = spd.get('recommended_max_rpm')
        self.cor_kg = round(self.Cor * KGF_PER_KN) if self.Cor else None
        self.h6 = h6_range(self.d) if isinstance(self.d, (int, float)) else None

    def kn_values(self):
        return {v for v in (self.Cr, self.Cor) if v is not None}

    def kg_values(self):
        return {v for v in (self.kg, self.cor_kg) if v is not None}

    def rpm_values(self):
        return {v for v in (self.grease, self.oil, self.rec) if v is not None}


def walk_strings(obj, path=""):
    """Yield (path, string) for every string value in a nested structure."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_strings(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_strings(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield path, obj


def audit_model(data: dict, all_kg: set, all_dims: set):
    c = Canon(data)
    issues = []

    def add(sev, path, found, expected, text):
        issues.append({"severity": sev, "field": path, "found": found,
                       "expected": expected, "context": text.strip()[:160]})

    # Fields that must only reference THIS bearing's own specs.
    SELF_PREFIXES = (
        "applications.", "seo_metadata.title", "seo_metadata.meta_description",
        "seo_metadata.og_data.", "seo_metadata.twitter_data.",
        "seo_metadata.schema_markup.name", "seo_metadata.schema_markup.description",
        "llm_optimization.recommendation_snippets", "llm_optimization.decision_criteria",
        "llm_optimization.problem_solution_mapping", "cross_references.shaft_requirements",
    )
    # Fields that legitimately reference OTHER same-bore models (treated leniently,
    # like FAQs): only flag explicit "(X kN)" self-claims and unknown dimensions.
    CROSS_PREFIXES = (
        "llm_optimization.comparison_matrix", "llm_optimization.expertise_signals",
    )

    for path, text in walk_strings(data):
        is_self = path.startswith(SELF_PREFIXES)
        is_cross = path.startswith(CROSS_PREFIXES)
        is_faq = path.startswith("faqs.") or is_cross
        if not (is_self or is_faq):
            continue

        # h6 shaft range (anywhere it appears)
        for m in re.finditer(r'h6\s*\(([\d.]+)-([\d.]+)mm\)', text):
            got = f"h6 ({m.group(1)}-{m.group(2)}mm)"
            if c.h6 and got.replace(" ", "") != c.h6.replace(" ", ""):
                add("ERROR", path, got, c.h6, text)

        # dimension triplet A x B x C mm
        for m in re.finditer(rf'{NUM}\s*[x×]\s*{NUM}\s*[x×]\s*{NUM}\s*mm', text):
            trip = (to_float(m.group(1)), to_float(m.group(2)), to_float(m.group(3)))
            if c.d and trip != (c.d, c.D, c.B):
                if is_self or trip not in all_dims:
                    add("ERROR" if is_self else "REVIEW", path,
                        "×".join(str(int(x)) for x in trip),
                        f"{int(c.d)}×{int(c.D)}×{int(c.B)}", text)

        if not is_self:
            # For FAQs only check explicit "(X.XX kN)" self-claims, dims and h6.
            for m in re.finditer(rf'\(\s*{NUM}\s*kN\s*\)', text):
                val = to_float(m.group(1))
                if val not in c.kn_values():
                    add("REVIEW", path, f"{m.group(1)}kN",
                        f"Cr={c.Cr} / Cor={c.Cor}", text)
            continue

        # --- self-referential numeric checks ---
        for m in re.finditer(rf'{NUM}\s*kN', text):
            val = to_float(m.group(1))
            if not any(approx(val, x, 0.05) for x in c.kn_values()):
                add("ERROR", path, f"{m.group(1)}kN",
                    f"Cr={c.Cr} or Cor={c.Cor}", text)

        for m in re.finditer(rf'{NUM}\s*kg', text):
            val = to_float(m.group(1))
            if not any(approx(val, x, 1.5) for x in c.kg_values()):
                add("ERROR", path, f"{m.group(1)}kg",
                    f"{c.kg}kg (dyn) / {c.cor_kg}kg (static)", text)

        for m in re.finditer(rf'{NUM}\s*RPM', text, re.IGNORECASE):
            val = to_float(m.group(1))
            if not any(approx(val, x, 50) for x in c.rpm_values()):
                add("ERROR", path, f"{m.group(1)} RPM",
                    f"grease={c.grease}/oil={c.oil}/rec={c.rec}", text)

    return c, issues


def main():
    models_dir = Path("models")
    files = sorted(models_dir.glob("*.json"))
    if not files:
        print("No model files found (run from project root).")
        sys.exit(1)

    all_data = {}
    for f in files:
        try:
            all_data[f.stem] = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  ! could not parse {f.name}: {e}")

    all_kg = {Canon(d).kg for d in all_data.values() if Canon(d).kg}
    all_dims = {(Canon(d).d, Canon(d).D, Canon(d).B) for d in all_data.values()
                if Canon(d).d}

    only = sys.argv[1] if len(sys.argv) > 1 else None
    report = {}
    tot_err = tot_rev = files_with_err = 0

    for stem, data in all_data.items():
        if only and stem != only:
            continue
        c, issues = audit_model(data, all_kg, all_dims)
        errs = [i for i in issues if i["severity"] == "ERROR"]
        revs = [i for i in issues if i["severity"] == "REVIEW"]
        if issues:
            report[stem] = issues
        tot_err += len(errs)
        tot_rev += len(revs)
        if errs:
            files_with_err += 1
        if only or errs:
            print(f"\n=== {stem}  (Cr={c.Cr}kN Cor={c.Cor}kN {c.kg}kg | "
                  f"{c.d}×{c.D}×{c.B}mm | grease {c.grease}rpm | {c.h6}) ===")
            for i in errs + (revs if only else []):
                print(f"  [{i['severity']}] {i['field']}")
                print(f"      found: {i['found']}  expected: {i['expected']}")
                print(f"      ctx:   {i['context']}")

    out = Path("scripts/consistency_report.json")
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("\n" + "=" * 60)
    print(f"Models scanned: {len([s for s in all_data if not only or s == only])}")
    print(f"Files with ERROR-level issues: {files_with_err}")
    print(f"Total ERROR issues: {tot_err}   Total REVIEW issues: {tot_rev}")
    print(f"Full report written to {out}")


if __name__ == "__main__":
    main()

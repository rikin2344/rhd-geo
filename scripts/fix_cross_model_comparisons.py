#!/usr/bin/env python3
"""
Cross-model comparison fixer (bore/ID based)
=============================================

Compatibility & comparison are defined by BORE (ID): bearings that share the
same bore are the comparison/replacement family (e.g. 6204 / 6004 / 6304, all
20mm; for 3-digit miniatures the last digit is the bore, e.g. 689 -> 9mm).

This script, using only verified foundation data from every model file:
  1. Rebuilds cross_references.related_models = real same-bore family (fixes
     phantom entries that point to non-existent models).
  2. Regenerates llm_optimization.comparison_matrix.vs_smaller_bearing /
     vs_larger_bearing from the nearest same-bore neighbours (by OD), with
     their real Cr values.
  3. Regenerates the 'Performance Comparison' expertise signal on a same-bore
     basis.

Dry-run by default; pass --apply to write.  Optional single-model arg.
"""
import json
import glob
import sys
from pathlib import Path


def load_all():
    data = {}
    paths = {}
    for f in glob.glob("models/*.json"):
        d = json.loads(Path(f).read_text(encoding="utf-8"))
        key = str(d["model_number"])
        data[key] = d
        paths[key] = f
    return data, paths


def fmt_kn(v):
    return f"{v:.2f}" if v is not None else "?"


def main():
    apply = "--apply" in sys.argv
    only = next((a for a in sys.argv[1:] if not a.startswith("--")), None)
    data, paths = load_all()

    def bore(m):
        return data[m]["dimensions"]["bore_diameter_d_mm"]

    def OD(m):
        return data[m]["dimensions"]["outer_diameter_D_mm"]

    def Cr(m):
        return data[m]["load_ratings"]["dynamic_load_Cr_kN"]

    def Cor(m):
        return data[m]["load_ratings"]["static_load_Cor_kN"]

    # group by verified bore
    fams = {}
    for m in data:
        fams.setdefault(bore(m), []).append(m)
    for b in fams:
        fams[b].sort(key=OD)

    files_changed = 0
    for m, d in data.items():
        if only and m != only:
            continue
        b = bore(m)
        family = [x for x in fams[b] if x != m]
        # nearest smaller / larger by OD
        smaller = [x for x in family if OD(x) < OD(m)]
        larger = [x for x in family if OD(x) > OD(m)]
        S = max(smaller, key=OD) if smaller else None
        L = min(larger, key=OD) if larger else None

        changes = []

        # 1) related_models = real same-bore family (ordered by OD)
        cr_ref = d.setdefault("cross_references", {})
        old_rel = cr_ref.get("related_models", [])
        new_rel = family[:]  # all real same-bore models, OD-sorted
        if old_rel != new_rel:
            changes.append(("related_models", old_rel, new_rel))
            cr_ref["related_models"] = new_rel

        # 2) comparison_matrix
        cm = d.setdefault("llm_optimization", {}).setdefault("comparison_matrix", {})
        if S:
            vs_small = (f"Same {b}mm bore as the {S} but in a larger {OD(m)}mm OD body — "
                        f"the {m} delivers {fmt_kn(Cr(m))}kN dynamic vs {fmt_kn(Cr(S))}kN for "
                        f"the {S}, the higher-capacity option when the shaft stays {b}mm.")
        elif L:
            vs_small = (f"The {m} is the most compact {b}mm-bore bearing in this family "
                        f"({OD(m)}mm OD, {fmt_kn(Cr(m))}kN); the {L} adds load capacity on the "
                        f"same {b}mm shaft.")
        else:
            vs_small = (f"The {m} is the only {b}mm-bore bearing in this family "
                        f"({OD(m)}mm OD, {fmt_kn(Cr(m))}kN dynamic).")
        if L:
            vs_large = (f"Need more load on the same {b}mm shaft? The {L} ({OD(L)}mm OD, "
                        f"{fmt_kn(Cr(L))}kN) is the heavier-duty same-bore alternative to the "
                        f"{m} ({fmt_kn(Cr(m))}kN) — choose the {m} to save radial space.")
        elif S:
            vs_large = (f"The {m} is the highest-capacity {b}mm-bore bearing in this family "
                        f"({fmt_kn(Cr(m))}kN at {OD(m)}mm OD); step down to the {S} for a more "
                        f"compact fit on the same shaft.")
        else:
            vs_large = vs_small
        if cm.get("vs_smaller_bearing") != vs_small:
            changes.append(("comparison_matrix.vs_smaller_bearing", cm.get("vs_smaller_bearing"), vs_small))
            cm["vs_smaller_bearing"] = vs_small
        if cm.get("vs_larger_bearing") != vs_large:
            changes.append(("comparison_matrix.vs_larger_bearing", cm.get("vs_larger_bearing"), vs_large))
            cm["vs_larger_bearing"] = vs_large

        # 3) Performance Comparison expertise signal
        sig_list = ", ".join(family[:3]) if family else "none"
        ctx = ""
        if S and L:
            ctx = (f" — more capacity than the {S} ({fmt_kn(Cr(S))}kN) and less than the "
                   f"heavier-duty {L} ({fmt_kn(Cr(L))}kN)")
        elif S:
            ctx = f" — the highest-capacity {b}mm-bore option, above the {S} ({fmt_kn(Cr(S))}kN)"
        elif L:
            ctx = f" — the most compact {b}mm-bore option, below the {L} ({fmt_kn(Cr(L))}kN)"
        perf = (f"Shares the {b}mm bore (ID) with {sig_list}, so it can be considered where the "
                f"shaft is fixed at {b}mm. The {m} is rated {fmt_kn(Cr(m))}kN dynamic / "
                f"{fmt_kn(Cor(m))}kN static at {OD(m)}mm OD{ctx}.")
        for sig in d.get("llm_optimization", {}).get("expertise_signals", []):
            if isinstance(sig, dict) and sig.get("title") == "Performance Comparison":
                if sig.get("description") != perf:
                    changes.append(("expertise_signals[Performance Comparison]",
                                    sig.get("description"), perf))
                    sig["description"] = perf

        if changes:
            files_changed += 1
            if only or True:
                print(f"\n=== {m} (bore {b}mm | smaller={S} larger={L}) === {len(changes)} changes")
                for fld, old, new in changes:
                    if fld == "related_models":
                        print(f"  related_models: {old} -> {new}")
                    else:
                        print(f"  {fld}:\n     OLD: {str(old)[:130]}\n     NEW: {str(new)[:130]}")
        if apply and changes:
            Path(paths[m]).write_text(
                json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("\n" + "=" * 60)
    print(f"{'APPLIED' if apply else 'DRY-RUN'} | files changed: {files_changed}")
    if not apply:
        print("Re-run with --apply to write.")


if __name__ == "__main__":
    main()

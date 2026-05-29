# RHD GEO — Bearing Specification Pages (Generator + Deployer)

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository turns per-model bearing data (`models/*.json`) into static, SEO/GEO-optimized
HTML specification pages and deploys them to `rhdbearings.com/specs/...` via FTP.

Each model JSON → one web page with verified dimensions, load ratings, speed limits, FAQs,
same-bore (ID) replacement guidance, and structured data (`Product` + `FAQPage` + `BreadcrumbList`
JSON-LD) for Google rich results and LLM/AI citation (GEO).

> **Source of truth:** the top-level `dimensions`, `load_ratings`, and `speed_limits` blocks in
> each `models/<model>.json` file are the authoritative data. Everything else on the page (prose,
> metadata, schema, comparisons) must stay consistent with these blocks. The audit/fix scripts
> enforce this.

---

## 📦 Data flow

```
models/<model>.json                         # per-model data (source of truth)
        │
        ▼   scripts/generate_universal_bearing_pages.py   (non-miniature series)
            scripts/generate_miniature_pages.py           (3-digit miniatures)
        │   + webpages/templates/index_new_claude.html    (shared template)
        ▼
webpages/<Series>WebPage/internalpages/<model>/index.html   # generated page
        │
        ▼   (same scripts, --standalone-only)
deployment/<series>/.../<model>/index.html   # self-contained page (inline CSS, schema in <head>)
        │
        ▼   scripts/deploy_by_series.py  /  deployment/curl_upload.py   (FTP)
https://rhdbearings.com/specs/<series>/<model>/             # live
```

---

## ✅ Prerequisites & setup

```bash
# 1. Python 3.7+ and curl (curl is used for FTP uploads)
python3 --version
curl --version

# 2. Install Python dependencies
pip install -r requirements.txt        # requests, python-dotenv, etc.

# 3. Configure FTP credentials in .env (already present locally; do NOT commit secrets)
#    Required keys:
#      FTP_HOST=ftp.rhdbearings.com
#      FTP_PORT=21
#      FTP_USERNAME=rikin@rhdbearings.com
#      FTP_PASSWORD=********
#      FTP_ROOT_PATH=/public_html
```

> All generate/deploy commands are run **from the repository root** (`RHD GEO/`).

---

## 🚀 Common workflows

### A. Rebuild & redeploy ALL pages (after a data or template change)

Run generate → standalone for both pipelines, then deploy series by series.

```bash
# 1. Generate page HTML from JSON
python3 scripts/generate_universal_bearing_pages.py --generate-only   # all non-miniature series
python3 scripts/generate_miniature_pages.py        --generate-only    # 3-digit miniatures

# 2. Build self-contained deploy pages (inline CSS + schema)
python3 scripts/generate_universal_bearing_pages.py --standalone-only
python3 scripts/generate_miniature_pages.py        --standalone-only

# 3. Deploy ONE series at a time (recommended — robust against FTP timeouts)
python3 scripts/deploy_by_series.py 6000
python3 scripts/deploy_by_series.py 6200
python3 scripts/deploy_by_series.py 6300
python3 scripts/deploy_by_series.py 6800
python3 scripts/deploy_by_series.py 6900
python3 scripts/deploy_by_series.py 16000
python3 scripts/deploy_by_series.py 62200
python3 scripts/deploy_by_series.py 62300
python3 scripts/deploy_by_series.py miniature
python3 scripts/deploy_by_series.py specs

# 4. Refresh the sitemap (bumps <lastmod> so Google/AI recrawl) and upload it
python3 scripts/generate_sitemap.py            # writes deployment/sitemap-specs.xml
#   then upload it with working credentials (the script's built-in upload uses a stale user):
set -a; . ./.env; set +a
curl --ftp-create-dirs -T deployment/sitemap-specs.xml \
     -u "$FTP_USERNAME:$FTP_PASSWORD" \
     "ftp://$FTP_HOST/public_html/sitemap-specs.xml"
```

> `deploy_by_series.py` uses fast-failing curl (`--connect-timeout`/`--max-time`/`--retry`) so a
> single flaky page can't stall the whole batch. Prefer it over the all-at-once uploader.

### B. Build & deploy a SINGLE page (quick edit to one model)

```bash
# Regenerate + standalone for everything is cheap (~2s), or target the page's series:
python3 scripts/generate_universal_bearing_pages.py --generate-only --6200-series
python3 scripts/generate_universal_bearing_pages.py --standalone-only --6200-series

# Upload just that page:
python3 deployment/curl_upload.py --page 6204        # 4-digit / 5-digit model
python3 deployment/curl_upload.py --page 684         # 3-digit miniature
python3 deployment/curl_upload.py --page 6200        # a series main page
python3 deployment/curl_upload.py --page specs       # the specs hub
```

### C. Add a BRAND-NEW model

```bash
# 1. Create the data file. Easiest: copy a same-series model and edit the foundation blocks.
cp models/6204.json models/6221.json
#    Edit models/6221.json — at minimum the top-level:
#      model_number, dimensions{bore_diameter_d_mm, outer_diameter_D_mm, width_B_mm},
#      load_ratings{dynamic_load_Cr_kN, static_load_Cor_kN}, speed_limits{...},
#      and seo_metadata.canonical_url (use lowercase slug, e.g. /specs/6200-series/6221/)

# 2. Make every other field consistent with the foundation blocks (no guesswork):
python3 scripts/audit_model_consistency.py 6221          # report mismatches
python3 scripts/fix_model_consistency.py 6221            # dry-run
python3 scripts/fix_model_consistency.py 6221 --apply    # apply deterministic fixes

# 3. Refresh bore-based cross-model comparisons (related_models, comparison_matrix, etc.):
python3 scripts/fix_cross_model_comparisons.py --apply
python3 scripts/fix_faq_self_dimensions.py    --apply

# 4. Final consistency check (expect 0 ERROR-level issues):
python3 scripts/audit_model_consistency.py

# 5. Generate + standalone + deploy the new page:
python3 scripts/generate_universal_bearing_pages.py --generate-only --6200-series
python3 scripts/generate_universal_bearing_pages.py --standalone-only --6200-series
python3 deployment/curl_upload.py --page 6221

# 6. Regenerate + upload the sitemap so the new URL gets discovered (see workflow A, step 4).
```

---

## 🧪 Data consistency tooling

All numeric content (kN, kg, RPM, mm) must match each model's foundation blocks. These scripts
keep that true and never invent values — they only normalize against the verified blocks.

| Script | Purpose |
|---|---|
| `scripts/audit_model_consistency.py [model]` | Report numeric inconsistencies (ERROR = self-contradiction, REVIEW = legit cross-model reference) |
| `scripts/fix_model_consistency.py [model] [--apply]` | Deterministically rewrite prose/metadata to match the foundation blocks |
| `scripts/fix_cross_model_comparisons.py [model] [--apply]` | Rebuild `related_models`, `comparison_matrix`, and the "Performance Comparison" signal on a **bore/ID** basis |
| `scripts/fix_faq_self_dimensions.py [--apply]` | Fix dimension triplets inside a model's own FAQs (self-referential only) |

All fixers are **dry-run by default**; pass `--apply` to write.

---

## 🌐 Output & URL structure

- **199 model pages** + 9 series hubs + specs hub, all under `/specs/`:

```
https://rhdbearings.com/specs/                         # hub
https://rhdbearings.com/specs/6200-series/             # series page
https://rhdbearings.com/specs/6200-series/6204/        # model page
https://rhdbearings.com/specs/miniature-series/684/    # miniature model
```

- Canonical URLs are lowercase (`6200-series`, not `6200-Series`).
- Compatibility/replacement is grouped by **bore (ID)**: e.g. `6204`, `6004`, `6304` all have a
  20 mm bore. For 3-digit miniatures the last digit is the bore (e.g. `689` → 9 mm).

## 🔎 SEO / GEO features baked into every page

- `Product` JSON-LD (name, image, sku, mpn, brand, category) — no invalid `Offer` block
- `FAQPage` JSON-LD built from the model's FAQs (matches visible content)
- `BreadcrumbList` JSON-LD (Home → Series → Model)
- Canonical link, Open Graph + Twitter meta, meta description/keywords
- `deployment/llms.txt` → curated map for AI crawlers (ChatGPT/Claude/Perplexity), served at
  `https://rhdbearings.com/llms.txt`
- Two sitemaps, both referenced in `robots.txt`:
  - `sitemap_index.xml` (WordPress/RankMath — main site)
  - `sitemap-specs.xml` (this repo — the 199 spec pages)

## 📈 Search Console (do after each big redeploy)

1. GSC → **Indexing → Sitemaps** → submit `sitemap_index.xml` and `sitemap-specs.xml`.
2. GSC → **URL Inspection** → **Request Indexing** for priority models (608, 626, 625, 6204,
   6205, 6203, 6200, 6004, 6304, 6900, 684 …). Daily quota applies — spread over a few days.
3. Submit the same two sitemaps in **Bing Webmaster Tools** (covers Bing/Copilot).
4. Watch **Pages** (coverage) and **Performance** for `/specs/` URLs over 2–4 weeks.

---

## 📁 Key locations

```
models/                                   # per-model source JSON (source of truth)
webpages/templates/index_new_claude.html  # shared HTML template (Product/FAQ/Breadcrumb schema)
webpages/<Series>WebPage/internalpages/   # generated (non-standalone) pages
scripts/                                  # generators, audit/fix tools, sitemap, deployer
deployment/                               # standalone pages, curl_upload.py, sitemap-specs.xml, llms.txt
.env                                      # FTP credentials (not committed)
```

> A legacy `rhd_bearings/` Python package (catalog JSON generator) also exists, but the live
> spec-page pipeline is the `scripts/` + `deployment/` workflow documented above.

---

## 📞 Company information

**RHD Bearings**
- 🌐 https://rhdbearings.com
- 📧 sales@rhdenterprise.in  ·  OEM/Bulk: oemsales@rhdenterprise.in
- 📞 +91-9702081858
- 📍 203 Vihar Estate, Off. Saki Vihar Road, Next to Autohanger, Sakinaka, Andheri East, Mumbai 400072

## 📄 License

MIT — see [LICENSE](LICENSE).

---

*Static bearing specification pages generated from verified JSON data and optimized for SEO, rich
results, and LLM/AI citation (GEO).*

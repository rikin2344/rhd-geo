#!/usr/bin/env python3
"""
Deploy one series at a time, with fast-failing curl uploads + retries so a
single flaky FTP page can't stall the whole batch. Reuses curl_upload's path
logic for correct remote paths (incl. oddball model names).

Usage:
  python3 scripts/deploy_by_series.py 6000
  python3 scripts/deploy_by_series.py miniature
  python3 scripts/deploy_by_series.py specs
Series keys: 6000 6200 6300 6800 6900 16000 62200 62300 miniature specs
"""
import os
import sys
import glob
import subprocess
import importlib.util
from dotenv import load_dotenv

load_dotenv()

spec = importlib.util.spec_from_file_location("curl_upload", "deployment/curl_upload.py")
cu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cu)

USER = os.getenv("FTP_USERNAME", "rikin@rhdbearings.com")
PWD = os.getenv("FTP_PASSWORD")
HOST = os.getenv("FTP_HOST", "ftp.rhdbearings.com")


def model_pages_for(series: str):
    """Return the list of curl_upload page-keys for a series (models + main)."""
    pages = []
    if series == "miniature":
        for d in sorted(glob.glob("deployment/miniature-series-internal-pages/*")):
            if os.path.isdir(d):
                pages.append(os.path.basename(d))
        pages.append("miniature")  # main series page
    elif series == "specs":
        pages.append("specs")
    else:
        base = f"deployment/{series}-series/{series}-series-internal-pages-deployment/*"
        for d in sorted(glob.glob(base)):
            if os.path.isdir(d):
                pages.append(os.path.basename(d))
        pages.append(series)  # main series page
    return pages


def upload_one(page: str):
    local, remote, url = cu.get_upload_paths(page)
    if not local or not os.path.exists(local):
        return ("MISSING", page, local)
    cmd = [
        "curl", "-s", "--ftp-create-dirs",
        "--connect-timeout", "15", "--max-time", "75",
        "--retry", "2", "--retry-delay", "3",
        "-T", local, "-u", f"{USER}:{PWD}",
        f"ftp://{HOST}/public_html/{remote}",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return ("OK" if r.returncode == 0 else f"FAIL({r.returncode})", page, url)


def main():
    if not PWD:
        print("FTP_PASSWORD not set"); sys.exit(1)
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    series = sys.argv[1]
    pages = model_pages_for(series)
    print(f"=== {series}: {len(pages)} pages ===")
    ok, failed = [], []
    for p in pages:
        status, page, info = upload_one(p)
        flag = "OK " if status == "OK" else "!! "
        print(f"  {flag}{page:14} {status}")
        (ok if status == "OK" else failed).append(page)
    print(f"--- {series}: {len(ok)} ok, {len(failed)} failed ---")
    if failed:
        print("  failed:", failed)
        sys.exit(2)


if __name__ == "__main__":
    main()

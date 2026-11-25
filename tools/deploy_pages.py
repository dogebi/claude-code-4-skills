#!/usr/bin/env python3
"""Publish index.html into the dogebi.github.io hub via the Git Data API.

The hub carries ~168 MB of other projects, so this never clones it:
blob -> tree (on top of the current commit) -> commit -> ref update, with a
final read-back that proves the published blob is the one we built.

    python3 tools/deploy_pages.py --dry-run
    python3 tools/deploy_pages.py
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
from typing import Optional

OWNER = "dogebi"
REPO = "dogebi.github.io"
BRANCH = "master"
FOLDER = "claude-code-4-skills"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAGE = os.path.join(ROOT, "index.html")
LIVE = f"https://{OWNER}.github.io/{FOLDER}/"


def gh(args: list, stdin: Optional[str] = None) -> str:
    proc = subprocess.run(["gh", *args], input=stdin, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"gh {' '.join(args)} failed:\n{proc.stderr.strip()}")
    return proc.stdout


def api(path: str, method: Optional[str] = None, payload: Optional[dict] = None):
    args = ["api", path]
    if method:
        args += ["-X", method]
    body = None
    if payload is not None:
        args += ["--input", "-"]
        body = json.dumps(payload)
    out = gh(args, body)
    return json.loads(out) if out.strip() else {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(PAGE):
        sys.exit("index.html missing")
    raw = open(PAGE, "rb").read()
    if len(raw) < 10_000:
        sys.exit("index.html looks too small; refusing to publish")
    if "Claude Code" not in raw.decode("utf-8", "replace"):
        sys.exit("index.html does not look like this project; refusing to publish")
    print(f"local: {len(raw) / 1024:.1f} KiB")

    try:
        current = api(f"repos/{OWNER}/{REPO}/contents/{FOLDER}/index.html?ref={BRANCH}")
        print(f"remote: {FOLDER}/index.html {current['size']} bytes")
    except SystemExit:
        print(f"remote: {FOLDER}/index.html absent")

    if args.dry_run:
        print(f"dry run: would publish {LIVE}")
        return 0

    ref = api(f"repos/{OWNER}/{REPO}/git/ref/heads/{BRANCH}")
    parent = ref["object"]["sha"]
    print(f"parent: {parent[:10]}")

    blob = api(f"repos/{OWNER}/{REPO}/git/blobs", "POST", {
        "content": base64.b64encode(raw).decode("ascii"),
        "encoding": "base64",
    })
    print(f"blob: {blob['sha'][:10]}")

    tree = api(f"repos/{OWNER}/{REPO}/git/trees", "POST", {
        "base_tree": parent,
        "tree": [{
            "path": f"{FOLDER}/index.html",
            "mode": "100644",
            "type": "blob",
            "sha": blob["sha"],
        }],
    })
    print(f"tree: {tree['sha'][:10]}")

    commit = api(f"repos/{OWNER}/{REPO}/git/commits", "POST", {
        "message": "claude-code-4-skills: publish field notes",
        "tree": tree["sha"],
        "parents": [parent],
    })
    print(f"commit: {commit['sha'][:10]}")

    api(f"repos/{OWNER}/{REPO}/git/refs/heads/{BRANCH}", "PATCH", {
        "sha": commit["sha"], "force": False,
    })

    check = api(f"repos/{OWNER}/{REPO}/git/ref/heads/{BRANCH}")
    if check["object"]["sha"] != commit["sha"]:
        sys.exit("ref update did not take effect")
    published = api(f"repos/{OWNER}/{REPO}/contents/{FOLDER}/index.html?ref={BRANCH}")
    if published.get("sha") != blob["sha"]:
        sys.exit("published file does not match the built blob")
    print(f"verified: {published['size']} bytes")
    print(f"live (Pages rebuilds in ~1 min): {LIVE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

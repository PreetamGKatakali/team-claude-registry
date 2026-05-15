#!/usr/bin/env python3
"""
Run from the root of the registry repo to regenerate manifest.json.
Usage: python generate-manifest.py [--bump-version agents/my-agent]
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent

ITEM_FILES = {
    "agents": "CLAUDE.md",
    "skills": "SKILL.md",
    "hooks":  "hook.json",
}

MANIFEST_FILE = ROOT / "manifest.json"


def sha12(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def discover_items() -> dict:
    items = {}
    for cat, filename in ITEM_FILES.items():
        cat_dir = ROOT / cat
        if not cat_dir.exists():
            continue
        for item_dir in sorted(cat_dir.iterdir()):
            if not item_dir.is_dir():
                continue
            f = item_dir / filename
            if not f.exists():
                print(f"  WARN: {f} not found, skipping {cat}/{item_dir.name}")
                continue
            items[f"{cat}/{item_dir.name}"] = sha12(f)
    return items


def load_existing() -> dict:
    if MANIFEST_FILE.exists():
        return json.loads(MANIFEST_FILE.read_text())
    return {"version": "1.0.0", "items": {}}


def bump_patch(version: str) -> str:
    parts = version.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts)


def main():
    bump_keys = set()
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--bump-version" and i + 1 < len(args):
            bump_keys.add(args[i + 1])
            i += 2
        else:
            i += 1

    existing = load_existing()
    old_items = existing.get("items", {})
    new_items_shas = discover_items()

    new_items = {}
    changed = []

    for key, sha in new_items_shas.items():
        old = old_items.get(key)
        if old is None:
            # New item — start at 1.0.0
            new_items[key] = {"version": "1.0.0", "sha": sha}
            changed.append(f"  ADD    {key} @ 1.0.0")
        elif old["sha"] != sha or key in bump_keys:
            # Changed — bump patch version
            new_ver = bump_patch(old["version"])
            new_items[key] = {"version": new_ver, "sha": sha}
            changed.append(f"  UPDATE {key}  {old['version']} → {new_ver}")
        else:
            new_items[key] = old

    removed = [k for k in old_items if k not in new_items_shas]
    for key in removed:
        changed.append(f"  REMOVE {key}")

    manifest = {"version": existing["version"], "items": new_items}
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2) + "\n")

    if changed:
        print("manifest.json updated:")
        for line in changed:
            print(line)
    else:
        print("manifest.json is already up to date.")


if __name__ == "__main__":
    main()

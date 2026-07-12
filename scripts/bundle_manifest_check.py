#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
IGNORE_FILE = ROOT / ".clawhubignore"
MANIFEST_ITEM_RE = re.compile(r"^\s*-\s+`([^`]+)`\s*$")
EXPECTED_CLAWHUB_BUNDLE = [
    "LICENSE",
    "SKILL.md",
    "agents/openai.yaml",
    "references/anger-frustration-route.md",
    "references/confusion-route.md",
    "references/urgency-route.md",
]


def to_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_ignore_patterns() -> list[str]:
    return [
        line.strip()
        for line in IGNORE_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def ignored(path: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if pattern.endswith("/**"):
            prefix = pattern[:-3]
            if path == prefix or path.startswith(f"{prefix}/"):
                return True
        elif path == pattern:
            return True
    return False


def actual_bundle_files() -> list[str]:
    patterns = read_ignore_patterns()
    files: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = to_posix(path)
        parts = rel.split("/")
        if any(part.startswith(".") for part in parts):
            continue
        if "__pycache__" in parts or path.suffix == ".pyc":
            continue
        if ignored(rel, patterns):
            continue
        files.append(rel)
    return sorted(files)


def documented_bundle_files() -> list[str]:
    lines = SKILL.read_text(encoding="utf-8").splitlines()
    inside = False
    files: list[str] = []
    for line in lines:
        if line.strip() == "ClawHub publish now ships the Markdown-first skill bundle:":
            inside = True
            continue
        if inside and line.startswith("The GitHub repository keeps"):
            break
        if inside:
            match = MANIFEST_ITEM_RE.match(line)
            if match:
                files.append(match.group(1))
    return sorted(files)


def check_manifest() -> dict[str, Any]:
    actual = actual_bundle_files()
    documented = documented_bundle_files()
    missing_sources = [path for path in documented if not (ROOT / path).is_file()]
    return {
        "ok": actual == documented == EXPECTED_CLAWHUB_BUNDLE and not missing_sources,
        "actual_count": len(actual),
        "documented_count": len(documented),
        "missing_from_docs": sorted(set(actual) - set(documented)),
        "missing_from_bundle": sorted(set(documented) - set(actual)),
        "missing_sources": missing_sources,
        "actual": actual,
        "documented": documented,
        "expected": EXPECTED_CLAWHUB_BUNDLE,
    }


def stage_bundle(output: Path, target: str) -> dict[str, Any]:
    manifest = check_manifest()
    if not manifest["ok"]:
        raise ValueError("bundle manifest must pass before staging")

    output = output.resolve()
    if output in {ROOT, ROOT.parent}:
        raise ValueError("refusing to stage over the repository or its parent")
    if output.exists():
        if not output.is_dir():
            raise ValueError(f"staging path is not a directory: {output}")
        if any(output.iterdir()):
            raise ValueError(f"staging directory is not empty: {output}")

    selected = list(EXPECTED_CLAWHUB_BUNDLE)
    if target == "skillhub":
        selected.remove("LICENSE")

    output.mkdir(parents=True, exist_ok=True)
    for relative in selected:
        source = ROOT / relative
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    staged = sorted(
        path.relative_to(output).as_posix()
        for path in output.rglob("*")
        if path.is_file()
    )
    digest = hashlib.sha256()
    for relative in staged:
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update((output / relative).read_bytes())
        digest.update(b"\0")
    return {
        "ok": staged == sorted(selected),
        "target": target,
        "output": str(output),
        "files": staged,
        "count": len(staged),
        "sha256": digest.hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate or stage the explicit marketplace bundle allowlist.")
    parser.add_argument("--stage", type=Path, help="Copy only allowlisted files into this empty directory.")
    parser.add_argument("--target", choices=("clawhub", "skillhub"), default="clawhub")
    args = parser.parse_args()

    if args.stage:
        try:
            result = stage_bundle(args.stage, args.target)
        except ValueError as exc:
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
            return 1
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1

    result = check_manifest()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

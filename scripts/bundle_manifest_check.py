#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
IGNORE_FILE = ROOT / ".clawhubignore"
MANIFEST_ITEM_RE = re.compile(r"^\s*-\s+`([^`]+)`\s*$")

# Explicit allowlist is the release source of truth for the ClawHub/GitHub skill surface.
PUBLISHED_ALLOWLIST = [
    "LICENSE",
    "SKILL.md",
    "agents/openai.yaml",
    "references/anger-frustration-route.md",
    "references/confusion-route.md",
    "references/urgency-route.md",
]

# SkillHub.cn rejects LICENSE as an upload file type; keep license in SKILL.md frontmatter.
SKILLHUB_ALLOWLIST = [
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


def ignore_derived_bundle_files() -> list[str]:
    """Defense-in-depth view from .clawhubignore. Not the release source of truth."""
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


def allowlist_for_target(target: str) -> list[str]:
    if target == "skillhub":
        return list(SKILLHUB_ALLOWLIST)
    return list(PUBLISHED_ALLOWLIST)


def stage_bundle(stage_dir: Path, target: str = "clawhub") -> list[str]:
    if stage_dir.exists():
        shutil.rmtree(stage_dir)
    stage_dir.mkdir(parents=True, exist_ok=True)
    staged: list[str] = []
    for rel in allowlist_for_target(target):
        src = ROOT / rel
        if not src.is_file():
            raise FileNotFoundError(f"missing allowlisted file: {rel}")
        dest = stage_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        staged.append(rel)
    return sorted(staged)


def check_manifest() -> dict[str, Any]:
    allowlist = sorted(PUBLISHED_ALLOWLIST)
    documented = documented_bundle_files()
    ignore_derived = ignore_derived_bundle_files()
    missing_files = [rel for rel in allowlist if not (ROOT / rel).is_file()]
    ok = (
        allowlist == documented
        and allowlist == ignore_derived
        and not missing_files
    )
    return {
        "ok": ok,
        "source_of_truth": "PUBLISHED_ALLOWLIST",
        "allowlist": allowlist,
        "documented": documented,
        "ignore_derived": ignore_derived,
        "missing_files": missing_files,
        "missing_from_docs": sorted(set(allowlist) - set(documented)),
        "missing_from_allowlist": sorted(set(documented) - set(allowlist)),
        "ignore_extra": sorted(set(ignore_derived) - set(allowlist)),
        "ignore_missing": sorted(set(allowlist) - set(ignore_derived)),
        # Back-compat keys used by markdown_skill_audit.
        "actual": ignore_derived,
        "actual_count": len(ignore_derived),
        "documented_count": len(documented),
        "missing_from_bundle": sorted(set(documented) - set(ignore_derived)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check or stage the published skill bundle.")
    parser.add_argument("--stage", type=Path, help="Stage allowlisted files into this directory")
    parser.add_argument(
        "--target",
        choices=("clawhub", "skillhub"),
        default="clawhub",
        help="Marketplace target label for staged output metadata",
    )
    args = parser.parse_args()

    result = check_manifest()
    if args.stage:
        expected = sorted(allowlist_for_target(args.target))
        staged = stage_bundle(args.stage, target=args.target)
        result["staged"] = staged
        result["stage_dir"] = str(args.stage)
        result["target"] = args.target
        result["expected_for_target"] = expected
        result["stage_ok"] = staged == expected
        # SkillHub uses a subset allowlist; clawhub/git surface still must match full allowlist.
        if args.target == "clawhub":
            result["ok"] = result["ok"] and result["stage_ok"]
        else:
            result["ok"] = result["stage_ok"] and not result.get("missing_files")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

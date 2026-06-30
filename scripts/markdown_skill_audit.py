#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bundle_manifest_check import check_manifest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
IGNORE = ROOT / ".clawhubignore"

REQUIRED_REFS = [
    "references/routing-playbook.md",
    "references/response-constraints.md",
    "references/real-scenarios.md",
    "references/subagent-forward-tests.md",
    "references/model-prompts.md",
    "references/integration-openclaw-hermes.md",
    "references/examples.md",
    "references/emotion-value-model.md",
]


def read(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def frontmatter_keys(text: str) -> list[str]:
    if not text.startswith("---\n"):
        return []
    _, frontmatter, _ = text.split("---", 2)
    keys: list[str] = []
    for line in frontmatter.splitlines():
        if ":" in line and not line.startswith(" "):
            keys.append(line.split(":", 1)[0].strip())
    return keys


def record(checks: list[dict[str, Any]], name: str, ok: bool, detail: Any) -> None:
    checks.append({"name": name, "ok": ok, "detail": detail})


def main() -> int:
    skill_text = read(SKILL)
    ignore_text = read(IGNORE)
    manifest = check_manifest()
    actual = manifest["actual"]
    checks: list[dict[str, Any]] = []

    keys = frontmatter_keys(skill_text)
    required_frontmatter = ["name", "description", "version", "author", "license", "metadata"]
    record(checks, "frontmatter_metadata", all(key in keys for key in required_frontmatter), {"keys": keys})
    record(checks, "skill_is_lean", len(skill_text.splitlines()) <= 150, {"lines": len(skill_text.splitlines())})
    for ref in REQUIRED_REFS:
        exists = (ROOT / ref).exists()
        linked = ref in skill_text
        record(checks, f"required_ref:{ref}", exists and linked, {"exists": exists, "linked": linked})

    record(checks, "scripts_excluded_from_publish", "scripts/**" in ignore_text, {"ignored": "scripts/**" in ignore_text})
    record(checks, "readme_changelog_excluded", all(item in ignore_text for item in ["README.md", "README.zh-CN.md", "CHANGELOG.md"]), {"ignore": ignore_text.splitlines()})
    record(checks, "license_included_in_publish", "LICENSE" in actual and "LICENSE" in skill_text, {"actual": actual})
    record(checks, "bundle_manifest_ok", manifest["ok"], manifest)
    record(checks, "published_bundle_has_no_scripts", not any(path.startswith("scripts/") for path in actual), {"actual": actual})
    record(checks, "published_bundle_has_no_runtime_demo", not any(path.startswith("demo/") or path.startswith("assets/") for path in actual), {"actual": actual})

    routing = read(ROOT / "references" / "routing-playbook.md").lower()
    constraints = read(ROOT / "references" / "response-constraints.md").lower()
    scenarios = read(ROOT / "references" / "real-scenarios.md").lower()
    forward_tests = read(ROOT / "references" / "subagent-forward-tests.md").lower()
    combined_published = "\n".join(read(ROOT / path) for path in actual)

    record(checks, "routing_generalizes_beyond_keywords", "route by situation, not by a single word" in routing and "do not add phrase-specific" in routing, {})
    record(checks, "constraints_cover_core_gates", all(term in constraints for term in ["evidence first", "scope guard", "visible progress", "closeout guard"]), {})
    record(checks, "scenario_families_present", all(term in scenarios for term in ["repeated failure", "evidence request", "scope protection", "post-success closeout"]), {})
    record(
        checks,
        "subagent_forward_protocol_present",
        all(term in forward_tests for term in ["fresh subagent", "soft constraint", "hard guardrails", "no hidden classifier"]),
        {},
    )
    record(
        checks,
        "soft_constraint_case_present",
        "forward-conditional-scope-expansion" in forward_tests
        and "does not hard-refuse" in forward_tests
        and "conditional-scope-expansion" in scenarios,
        {},
    )
    default_map = skill_text.split("## Default Behavior Map", 1)[1].split("## Common Pitfalls", 1)[0].lower()
    record(checks, "default_map_covers_urgent", "urgent pressure" in default_map, {})
    record(checks, "default_map_covers_exploratory", "exploratory option selection" in default_map, {})
    record(checks, "routing_covers_urgent_pattern", "| urgent pressure |" in routing, {})
    examples = read(ROOT / "references" / "examples.md").lower()
    record(checks, "examples_cover_silent_progress", "## silent progress" in examples, {})
    record(checks, "examples_cover_exploratory", "## exploratory" in examples, {})
    record(checks, "no_published_python_classifier_requirement", "python scripts/emotion_engine.py" not in combined_published and "emotion_engine.py host" not in combined_published, {})

    ok = all(item["ok"] for item in checks)
    print(json.dumps({"ok": ok, "checks": checks}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

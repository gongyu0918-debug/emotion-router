#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bundle_manifest_check import check_manifest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
ROUTES = ROOT / "references" / "emotion-routes.md"
IGNORE = ROOT / ".clawhubignore"


ROUTES_EXPECTED = {
    "urgency": ["fastest minimal path", "fastest minimal verification", "next checkpoint"],
    "anger": ["stop the damage", "failing point", "smallest repair path"],
    "confusion": ["what is being done now", "blocked", "next step"],
}

BANNED_RUNTIME_REQUIREMENTS = [
    "must run python",
    "requires python",
    "run scripts/emotion_engine.py",
    "load durable memory",
    "read user profile",
    "persist calibration",
    "score the user",
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


def frontmatter_value(text: str, key: str) -> str:
    if not text.startswith("---\n"):
        return ""
    _, frontmatter, _ = text.split("---", 2)
    prefix = f"{key}:"
    for line in frontmatter.splitlines():
        if line.startswith(prefix):
            return line.split(":", 1)[1].strip().strip('"')
    return ""


def record(checks: list[dict[str, Any]], name: str, ok: bool, detail: Any) -> None:
    checks.append({"name": name, "ok": ok, "detail": detail})


def contains_all(text: str, terms: list[str]) -> bool:
    normalized = text.lower()
    return all(term.lower() in normalized for term in terms)


def main() -> int:
    skill_text = read(SKILL)
    routes_text = read(ROUTES)
    ignore_text = read(IGNORE)
    manifest = check_manifest()
    actual = manifest["actual"]
    combined_published = "\n".join(read(ROOT / path) for path in actual)
    combined_lower = combined_published.lower()
    checks: list[dict[str, Any]] = []

    keys = frontmatter_keys(skill_text)
    required_frontmatter = ["name", "description", "version", "author", "license", "metadata"]
    record(checks, "frontmatter_metadata", all(key in keys for key in required_frontmatter), {"keys": keys})
    record(checks, "version_2_0_0", frontmatter_value(skill_text, "version") == "2.0.0", {"version": frontmatter_value(skill_text, "version")})
    record(checks, "skill_is_lean", len(skill_text.splitlines()) <= 110, {"lines": len(skill_text.splitlines())})

    description = frontmatter_value(skill_text, "description").lower()
    record(
        checks,
        "description_has_trigger_boundary",
        all(term in description for term in ["current user prompt", "urgency", "anger/frustration", "confusion"]),
        {"description": frontmatter_value(skill_text, "description")},
    )
    record(checks, "single_route_reference_linked", ROUTES.exists() and "references/emotion-routes.md" in skill_text, {"exists": ROUTES.exists()})

    for route, required_terms in ROUTES_EXPECTED.items():
        record(checks, f"route_present:{route}", route in routes_text.lower(), {})
        record(checks, f"route_behavior:{route}", contains_all(routes_text, required_terms), {"required": required_terms})

    record(
        checks,
        "priority_order",
        "1. Urgency\n2. Anger or frustration\n3. Confusion" in skill_text,
        {},
    )
    record(checks, "signals_are_not_hard_keywords", "no single keyword is a hard trigger" in skill_text and "not hard keyword" in routes_text.lower(), {})
    record(
        checks,
        "no_complete_keyword_or_profanity_wordlist",
        contains_all(skill_text + "\n" + routes_text, ["no route requires a complete keyword", "not a wordlist to complete", "do not build or require a profanity wordlist", "semantic judgment"]),
        {},
    )
    record(
        checks,
        "content_mentions_do_not_trigger",
        contains_all(skill_text + "\n" + routes_text, ["content mentions alone", "field names", "research topics", "urgentflag", "profanity research", "ordinary work by default", "use judgment"]),
        {},
    )
    record(checks, "agent_has_no_real_emotions", "agent does not have real emotions" in skill_text.lower(), {})
    record(checks, "negative_pressure_risk_stated", contains_all(skill_text, ["defensive replies", "over-explaining", "guessing", "drifting", "expanding scope"]), {})

    banned_hits = [term for term in BANNED_RUNTIME_REQUIREMENTS if term in combined_lower]
    record(checks, "no_runtime_or_memory_requirement", not banned_hits, {"hits": banned_hits})
    record(
        checks,
        "explicit_no_memory_or_agents_scope",
        contains_all(skill_text, ["do not inspect", "agents.md", "durable memory", "user profiles", "old calibration state"]),
        {},
    )
    record(checks, "scripts_excluded_from_publish", "scripts/**" in ignore_text and not any(path.startswith("scripts/") for path in actual), {"actual": actual})
    record(checks, "bundle_manifest_ok", manifest["ok"], manifest)
    record(checks, "published_bundle_is_light", actual == ["LICENSE", "SKILL.md", "agents/openai.yaml", "references/emotion-routes.md"], {"actual": actual})
    record(checks, "legacy_refs_excluded", all(path not in actual for path in ["references/routing-playbook.md", "references/response-constraints.md", "references/emotion-policy-matrix.md"]), {"actual": actual})

    ok = all(item["ok"] for item in checks)
    print(json.dumps({"ok": ok, "checks": checks}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

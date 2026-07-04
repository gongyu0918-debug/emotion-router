#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bundle_manifest_check import check_manifest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
IGNORE = ROOT / ".clawhubignore"

ROUTE_FILES = {
    "urgency": ROOT / "references" / "urgency-route.md",
    "anger": ROOT / "references" / "anger-frustration-route.md",
    "confusion": ROOT / "references" / "confusion-route.md",
}

EXPECTED_BUNDLE = [
    "LICENSE",
    "SKILL.md",
    "agents/openai.yaml",
    "references/anger-frustration-route.md",
    "references/confusion-route.md",
    "references/urgency-route.md",
]

ROUTES_EXPECTED = {
    "urgency": ["fastest minimal path", "fastest minimal verification", "remaining risks last"],
    "anger": ["stop the damage", "failing point", "smallest repair path", "profanity wordlist"],
    "confusion": ["what is being done now", "blocked", "next concrete step", "at most one blocking question"],
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
    normalized = " ".join(text.lower().split())
    return all(term.lower() in normalized for term in terms)


def main() -> int:
    skill_text = read(SKILL)
    route_texts = {name: read(path) for name, path in ROUTE_FILES.items()}
    all_routes_text = "\n".join(route_texts.values())
    ignore_text = read(IGNORE)
    manifest = check_manifest()
    actual = manifest["actual"]
    combined_published = "\n".join(read(ROOT / path) for path in actual)
    combined_lower = combined_published.lower()
    checks: list[dict[str, Any]] = []

    keys = frontmatter_keys(skill_text)
    required_frontmatter = ["name", "description", "version", "author", "license", "metadata"]
    record(checks, "frontmatter_metadata", all(key in keys for key in required_frontmatter), {"keys": keys})
    record(checks, "version_2_0_1", frontmatter_value(skill_text, "version") == "2.0.1", {"version": frontmatter_value(skill_text, "version")})
    record(checks, "skill_entrypoint_is_lean", len(skill_text.splitlines()) <= 80, {"lines": len(skill_text.splitlines())})

    description = frontmatter_value(skill_text, "description").lower()
    record(
        checks,
        "description_has_trigger_boundary",
        all(term in description for term in ["current prompt", "clear urgency wording", "strong anger/frustration signals", "profanity", "repeated failure/blame", "workflow confusion", "neutral commands", "ordinary technical explanations", "content-only mentions"]),
        {"description": frontmatter_value(skill_text, "description")},
    )
    record(
        checks,
        "progressive_route_references_linked",
        all(path.exists() and path.relative_to(ROOT).as_posix() in skill_text for path in ROUTE_FILES.values()),
        {"routes": [path.relative_to(ROOT).as_posix() for path in ROUTE_FILES.values()]},
    )
    record(checks, "old_aggregate_route_not_linked", "references/emotion-routes.md" not in skill_text and not (ROOT / "references" / "emotion-routes.md").exists(), {})

    record(
        checks,
        "skill_does_not_duplicate_route_details",
        "## Signal Examples" not in skill_text and "## Three Routes" not in skill_text and "| User-side signal |" not in skill_text,
        {},
    )

    for route, required_terms in ROUTES_EXPECTED.items():
        route_text = route_texts[route]
        record(checks, f"route_present:{route}", f"# {route}".split()[1].lower() in route_text.lower() or route in route_text.lower(), {})
        record(checks, f"route_sections:{route}", contains_all(route_text, ["## signals", "## non-triggers", "## prompt pattern", "## overlap rules", "## forbidden behavior"]), {})
        record(checks, f"route_behavior:{route}", contains_all(route_text, required_terms), {"required": required_terms})

    record(
        checks,
        "priority_order",
        "1. Urgency\n2. Anger or frustration\n3. Confusion" in skill_text,
        {},
    )
    record(
        checks,
        "trigger_cues_are_clear_but_not_complete_wordlists",
        contains_all(skill_text + "\n" + all_routes_text, ["clear speed", "priority wording", "not a complete keyword list", "strong active anger/frustration signals", "profanity list", "soft cues and context", "soft router"]),
        {},
    )
    record(
        checks,
        "progressive_loading_does_not_read_legacy_refs",
        contains_all(skill_text, ["do not compare against or load unrelated route files", "source path", "published bundle", "legacy material", "must not be read for routing"]),
        {},
    )
    record(
        checks,
        "no_complete_keyword_or_profanity_wordlist",
        contains_all(skill_text + "\n" + all_routes_text, ["not hard keyword triggers", "not a wordlist to complete", "do not build or require a profanity wordlist", "semantic judgment"]),
        {},
    )
    record(
        checks,
        "content_mentions_do_not_trigger_by_default",
        contains_all(skill_text + "\n" + all_routes_text, ["content mentions alone", "ordinary work by default", "field", "research", "quoted angry text"]),
        {},
    )
    record(
        checks,
        "ordinary_work_default_prevents_overrouting",
        contains_all(skill_text, ["trigger cautiously", "field name", "neutral command", "ordinary technical explanation request", "stop at this file", "ordinary work"]),
        {},
    )
    record(
        checks,
        "neutral_command_does_not_trigger_frustration",
        contains_all(route_texts["anger"], ["a single imperative is not enough", "neutral command", "task constraint", "normal coding instruction", "does not challenge", "repeated imperatives alone"]),
        {},
    )
    record(
        checks,
        "confusion_boundary_yields_to_frustration",
        contains_all(route_texts["confusion"], ["seeking orientation", "blame", "repeated failure pressure", "loss of trust", "use anger/frustration instead"]),
        {},
    )
    record(
        checks,
        "ordinary_explanation_does_not_trigger_confusion",
        contains_all(route_texts["confusion"], ["ordinary technical explanation request", "what does this error mean", "lost workflow orientation", "conflicting instructions", "mismatch with the current step"]),
        {},
    )
    record(checks, "agent_has_no_real_emotions", "agent does not have real emotions" in skill_text.lower(), {})
    record(checks, "negative_pressure_risk_stated", contains_all(skill_text, ["defensive replies", "over-explaining", "guessing", "drifting", "expanding scope"]), {})

    banned_hits = [term for term in BANNED_RUNTIME_REQUIREMENTS if term in combined_lower]
    record(checks, "no_runtime_or_memory_requirement", not banned_hits, {"hits": banned_hits})
    record(
        checks,
        "explicit_no_memory_or_agents_scope",
        contains_all(skill_text, ["do not inspect", "agents.md", "durable memory", "user profiles", "old calibration"]),
        {},
    )
    record(checks, "scripts_excluded_from_publish", "scripts/**" in ignore_text and not any(path.startswith("scripts/") for path in actual), {"actual": actual})
    record(checks, "bundle_manifest_ok", manifest["ok"], manifest)
    record(checks, "published_bundle_is_progressive", actual == EXPECTED_BUNDLE, {"actual": actual, "expected": EXPECTED_BUNDLE})
    record(checks, "legacy_refs_excluded", all(path not in actual for path in ["references/emotion-routes.md", "references/routing-playbook.md", "references/response-constraints.md", "references/emotion-policy-matrix.md"]), {"actual": actual})

    ok = all(item["ok"] for item in checks)
    print(json.dumps({"ok": ok, "checks": checks}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

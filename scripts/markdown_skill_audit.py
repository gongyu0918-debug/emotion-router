#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from bundle_manifest_check import PUBLISHED_ALLOWLIST, check_manifest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
OPENAI_YAML = ROOT / "agents" / "openai.yaml"
ROUTE_FILES = {
    "urgency": ROOT / "references" / "urgency-route.md",
    "anger": ROOT / "references" / "anger-frustration-route.md",
    "confusion": ROOT / "references" / "confusion-route.md",
}

ALLOWED_FRONTMATTER = {"name", "description", "license", "metadata", "allowed-tools"}
REQUIRED_FRONTMATTER = {"name", "description", "license", "metadata"}
RUNTIME_RESIDUE = [
    "test command",
    "test result",
    "commit hash",
    "release gate",
    "maintainer",
    "published bundle",
    "clawhub",
    "skillhub",
    "scripts/",
    "reports/",
    "benchmark",
]
ROUTE_RESPONSE_TERMS = {
    "urgency": [
        "fastest usable path",
        "smallest available check",
        "remaining risk",
    ],
    "anger": [
        "stop the failing path",
        "stop writes",
        "smallest rollback or repair",
        "ask one question",
        "permission",
    ],
    "confusion": [
        "active step",
        "blocker",
        "next step",
        "at most one blocking question",
    ],
}
ROUTE_TRIGGER_TERMS = {
    "urgency": ["explicit speed", "do not trigger"],
    "anger": ["strong active", "do not trigger"],
    "confusion": ["workflow orientation", "do not trigger"],
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter_lines(text: str) -> list[str]:
    if not text.startswith("---\n"):
        return []
    return text.split("---", 2)[1].splitlines()


def frontmatter_keys(text: str) -> set[str]:
    return {
        line.split(":", 1)[0].strip()
        for line in frontmatter_lines(text)
        if ":" in line and line and not line.startswith(" ")
    }


def frontmatter_value(text: str, key: str) -> str:
    prefix = f"{key}:"
    for line in frontmatter_lines(text):
        if line.startswith(prefix):
            return line.split(":", 1)[1].strip().strip('"')
    return ""


def metadata_value(text: str, key: str) -> str:
    in_metadata = False
    prefix = f"  {key}:"
    for line in frontmatter_lines(text):
        if line == "metadata:":
            in_metadata = True
            continue
        if in_metadata and line and not line.startswith(" "):
            break
        if in_metadata and line.startswith(prefix):
            return line.split(":", 1)[1].strip().strip('"')
    return ""


def contains_all(text: str, terms: list[str]) -> bool:
    normalized = " ".join(text.lower().split())
    return all(term.lower() in normalized for term in terms)


def section_text(text: str, heading: str) -> str:
    marker = f"## {heading}"
    if marker not in text:
        return ""
    section = text.split(marker, 1)[1]
    return section.split("\n## ", 1)[0]


def record(checks: list[dict[str, Any]], name: str, ok: bool, detail: Any) -> None:
    checks.append({"name": name, "ok": ok, "detail": detail})


def main() -> int:
    skill = read(SKILL)
    routes = {name: read(path) for name, path in ROUTE_FILES.items()}
    openai_yaml = read(OPENAI_YAML)
    manifest = check_manifest()
    checks: list[dict[str, Any]] = []

    keys = frontmatter_keys(skill)
    record(
        checks,
        "frontmatter_schema",
        REQUIRED_FRONTMATTER <= keys <= ALLOWED_FRONTMATTER,
        {"keys": sorted(keys), "allowed": sorted(ALLOWED_FRONTMATTER)},
    )
    record(
        checks,
        "identity",
        frontmatter_value(skill, "name") == "emotion-skill"
        and frontmatter_value(skill, "license") == "MIT"
        and metadata_value(skill, "author") == "gongyu0918-debug"
        and bool(re.fullmatch(r"\d+\.\d+\.\d+", metadata_value(skill, "version"))),
        {
            "name": frontmatter_value(skill, "name"),
            "version": metadata_value(skill, "version"),
            "author": metadata_value(skill, "author"),
        },
    )

    description = frontmatter_value(skill, "description")
    record(
        checks,
        "description_boundary",
        contains_all(
            description,
            [
                "current prompt",
                "urgency",
                "anger/frustration",
                "confusion",
                "ordinary tasks",
                "neutral commands",
                "technical explanations",
                "content-only",
            ],
        ),
        {"description": description},
    )
    record(checks, "skill_is_lean", len(skill.splitlines()) <= 55, {"lines": len(skill.splitlines())})
    record(
        checks,
        "current_context_only",
        contains_all(
            skill,
            ["current work-state signal", "hidden history or memory", "emotion label", "semantic judgment", "not a keyword or profanity list"],
        ),
        {},
    )
    record(
        checks,
        "priority_and_damage_control",
        "1. Urgency\n2. Anger or frustration\n3. Confusion" in skill
        and contains_all(skill, ["permission challenge", "unauthorized change", "anger/frustration even when urgency"]),
        {},
    )
    record(
        checks,
        "one_reference_navigation",
        all(skill.count(path.relative_to(ROOT).as_posix()) == 1 for path in ROUTE_FILES.values())
        and "read exactly one reference" in skill.lower()
        and "without loading a reference" in skill.lower(),
        {},
    )

    runtime_text = "\n".join([skill, *routes.values()]).lower()
    residue_hits = [term for term in RUNTIME_RESIDUE if term in runtime_text]
    record(checks, "no_maintainer_or_test_residue", not residue_hits, {"hits": residue_hits})

    for name, route in routes.items():
        sections = ["## Trigger", "## Response", "## Avoid", "## Examples"]
        trigger = section_text(route, "Trigger")
        response = section_text(route, "Response")
        avoid = section_text(route, "Avoid")
        examples = section_text(route, "Examples")
        record(
            checks,
            f"route:{name}",
            len(route.splitlines()) <= 40
            and all(route.count(section) == 1 for section in sections)
            and contains_all(trigger, ROUTE_TRIGGER_TERMS[name])
            and contains_all(response, ROUTE_RESPONSE_TERMS[name])
            and avoid.count("- ") >= 2
            and examples.count("- ") >= 2,
            {
                "lines": len(route.splitlines()),
                "trigger_terms": ROUTE_TRIGGER_TERMS[name],
                "response_terms": ROUTE_RESPONSE_TERMS[name],
            },
        )

    implicit_match = re.search(r"(?m)^\s*allow_implicit_invocation:\s*(true|false)\s*$", openai_yaml)
    implicit_value = implicit_match.group(1) if implicit_match else ""
    short_match = re.search(r'(?m)^\s*short_description:\s*"([^"]+)"\s*$', openai_yaml)
    short_description = short_match.group(1) if short_match else ""
    record(
        checks,
        "openai_metadata",
        implicit_value == "true"
        and 25 <= len(short_description) <= 64
        and "$emotion-skill" in openai_yaml
        and not any(f"  {field}:" in openai_yaml for field in ["version", "author", "license"]),
        {"allow_implicit_invocation": implicit_value, "short_description": short_description},
    )
    record(
        checks,
        "bundle_manifest",
        manifest["ok"] and manifest["actual"] == sorted(PUBLISHED_ALLOWLIST),
        manifest,
    )

    ok = all(item["ok"] for item in checks)
    print(json.dumps({"ok": ok, "checks": checks}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

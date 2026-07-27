#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from bundle_manifest_check import PUBLISHED_ALLOWLIST, ROOT, stage_bundle


def expect_refusal(path: Path) -> str:
    try:
        stage_bundle(path)
    except ValueError as exc:
        return str(exc)
    raise AssertionError(f"unsafe staging path was accepted: {path}")


def main() -> int:
    root_error = expect_refusal(ROOT)
    ancestor_error = expect_refusal(ROOT.parent)
    repository_child_error = expect_refusal(ROOT / ".git" / "unsafe-stage-test")

    with tempfile.TemporaryDirectory(prefix="emotion-bundle-safety-") as temp:
        base = Path(temp)
        nonempty = base / "nonempty"
        nonempty.mkdir()
        sentinel = nonempty / "sentinel.txt"
        sentinel.write_text("must-survive", encoding="utf-8")
        nonempty_error = expect_refusal(nonempty)
        sentinel_preserved = sentinel.read_text(encoding="utf-8") == "must-survive"

        staged_dir = base / "staged"
        result = stage_bundle(staged_dir)
        fresh_stage_ok = (
            result["ok"]
            and result["files"] == sorted(PUBLISHED_ALLOWLIST)
            and len(result["sha256"]) == 64
        )

    output = {
        "ok": sentinel_preserved and fresh_stage_ok,
        "root_refusal": root_error,
        "ancestor_refusal": ancestor_error,
        "repository_child_refusal": repository_child_error,
        "nonempty_refusal": nonempty_error,
        "sentinel_preserved": sentinel_preserved,
        "fresh_stage_ok": fresh_stage_ok,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if output["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

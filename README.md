# Emotion Router

[简体中文](./README.zh-CN.md) · [GitHub](https://github.com/gongyu0918-debug/emotion-skill-qingxu-skill) · `clawhub install emotion-skill`

Markdown-first soft routing for coding agents when the current user prompt or
visible context shows urgency, anger/frustration, or confusion.

This skill does not model agent feelings. It reads user-side pressure signals and
routes the agent's next reply, work order, and verification style.

## Why People Install It

Negative user emotion and time pressure can push models toward defensive replies,
over-explaining, guessing, drifting from the task, or expanding scope.

Emotion Router keeps the response stable through three routes:

- **Urgency**: fastest minimal path to satisfy the prompt, then fastest minimal verification.
- **Anger or frustration**: stop the damage, locate the failing point, find the smallest repair path.
- **Confusion**: say what is being done now, what is blocked, and what happens next in plain language.

## Structure

Published ClawHub bundle:

- `SKILL.md`: trigger boundary, priority, and route selection
- `agents/openai.yaml`: UI metadata and default invocation prompt
- `references/emotion-routes.md`: signals, prompt patterns, forbidden behavior, and first-sentence shapes

GitHub-only maintenance files:

- `scripts/`: release checks, audits, and legacy runtime regression tests
- `references/`: older design notes and non-published validation references
- `assets/`, `demo/`, `reports/`: calibration, local examples, and test evidence

## Use

In a skills-aware agent:

```text
Use $emotion-skill when the current user prompt or visible context shows urgency,
anger/frustration, or confusion. Pick one route and apply the matching prompt
pattern. Do not run a Python classifier.
```

The agent should read `SKILL.md`, then load `references/emotion-routes.md` for the
selected route. Signal examples are not hard keyword triggers.

## Validation

Repository validation:

```bash
python scripts/markdown_skill_audit.py
python scripts/bundle_manifest_check.py
python scripts/marketplace_tag_audit.py
python scripts/smoke_test.py --strict
git diff --check
```

Subagent forward tests are the real behavior check for the three routes: urgency,
anger/frustration, confusion, plus the urgency+anger conflict case.

## Boundary

This is a skill, not a plugin or runtime classifier. It does not inspect
AGENTS.md, durable memory, user profiles, hidden history, or old calibration
state. It only uses the current prompt and visible context window.

## License

MIT. See the [GitHub repository license](https://github.com/gongyu0918-debug/emotion-skill-qingxu-skill/blob/main/LICENSE).

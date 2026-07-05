# Emotion Router

[简体中文](./README.zh-CN.md) · [GitHub](https://github.com/gongyu0918-debug/emotion-skill-qingxu-skill) · `clawhub install emotion-skill`

Markdown-first soft routing for coding agents when the current prompt shows
clear urgency wording, strong anger/frustration signals, or workflow confusion
about the current step, conflict, or mismatch.

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
- `LICENSE`: package license
- `agents/openai.yaml`: UI metadata and default invocation prompt
- `references/urgency-route.md`: urgency signals, non-triggers, response pattern, overlap rules, and examples
- `references/anger-frustration-route.md`: anger/frustration signals, non-triggers, response pattern, overlap rules, and examples
- `references/confusion-route.md`: confusion signals, non-triggers, response pattern, overlap rules, and examples

GitHub-only maintenance files:

- `scripts/`: release checks, audits, and legacy runtime regression tests
- `references/`: older design notes and non-published validation references
- `assets/`, `demo/`, `reports/`: calibration, local examples, and test evidence

## Use

In a skills-aware agent:

```text
Use $emotion-skill when the current prompt shows clear urgency wording, strong
anger/frustration signals such as profanity or repeated failure/blame, or
workflow confusion about the current step, conflict, or mismatch. Do not use it
for ordinary tasks, neutral commands, ordinary technical explanations, or
content-only emotion mentions.
```

The agent should read `SKILL.md`, choose one route by priority, then load only
the matching route reference. Trigger cues are explicit enough to avoid broad
over-routing, but they are not complete keyword or profanity wordlists.

## Validation

Repository validation:

```bash
python -B scripts/route_ablation_test.py
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

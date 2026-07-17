# Emotion Router

[简体中文](./README.zh-CN.md) · [GitHub](https://github.com/gongyu0918-debug/emotion-router) · `clawhub install emotion-skill` · `skillhub install emotion-skill`

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

Damage-control exception: if the user challenges permission or unauthorized
changes, anger/frustration wins even when urgency is also present. Stop first,
then repair fast.

## Structure

Published marketplace bundle:

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

The publish allowlist in `scripts/bundle_manifest_check.py` is the release source
of truth. `.clawhubignore` is defense in depth only.

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

2.0.5 Markdown skill release gates:

```bash
python -B scripts/route_ablation_test.py
python -B scripts/markdown_skill_audit.py
python -B scripts/bundle_manifest_check.py
python -B scripts/bundle_manifest_check.py --stage .release/clawhub --target clawhub
python -B scripts/bundle_manifest_check.py --stage .release/skillhub --target skillhub
python -B scripts/marketplace_tag_audit.py
git diff --check
```

`route_ablation_test.py` is a deterministic cue-contract proxy plus frozen-fixture
scoring. It is not a live model benchmark. Fresh subagent forward tests are the
behavior check for urgency, anger/frustration, confusion, damage-control overlap,
and non-trigger cases.

Legacy v1 runtime regression, optional and not evidence for 2.0.x skill behavior:

```bash
python -B scripts/smoke_test.py --strict
```

## Boundary

This is a skill, not a plugin or runtime classifier. It does not inspect
AGENTS.md, durable memory, user profiles, hidden history, or old calibration
state. It only uses the current prompt and visible context window.

## License

MIT. See the [GitHub repository license](https://github.com/gongyu0918-debug/emotion-router/blob/main/LICENSE).

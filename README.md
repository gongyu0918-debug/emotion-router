# Emotion Router

[简体中文](./README.zh-CN.md) · [GitHub](https://github.com/gongyu0918-debug/emotion-router) · `clawhub install emotion-skill` · `skillhub install emotion-skill`

A small Markdown-first soft router for coding agents. It reacts only to clear
current-work signals: urgency, strong anger/frustration, or workflow confusion.

## Purpose

Pressure can make an agent defend itself, over-explain, guess, drift, or widen
scope. Emotion Router maps that pressure to one of three short work patterns:

- **Urgency**: do the named task through the smallest usable path.
- **Anger or frustration**: stop the failing path and find the smallest repair.
- **Confusion**: state the active step, blocker, and next action plainly.

A permission challenge or unauthorized change always stops the current path
before speed is considered.

## Boundary

The router uses only the current prompt and visible context. It does not profile
the user, inspect durable memory, or classify emotion. Quotes, field names,
research topics, neutral commands, and ordinary technical explanations do not
trigger it by themselves.

The trigger cues are examples for semantic judgment, not complete keyword or
profanity lists.

## Package

The runtime package contains `SKILL.md`, `agents/openai.yaml`, and one reference
for each route. ClawHub also includes `LICENSE`; SkillHub omits that file because
the platform does not accept it. Repository scripts, reports, assets, and older
design references are maintenance material, not installed instructions.

Maintainer boundaries and validation commands are in [AGENTS.md](./AGENTS.md).

## License

MIT. See [LICENSE](./LICENSE).

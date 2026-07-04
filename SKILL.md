---
name: emotion-skill
description: 情绪路由：面向 coding agents 的中文友好 Markdown-first 工作状态路由。用于仓库调试、反复失败、evidence-first review、scope 收敛、静默等待、困惑澄清、紧急处理和完成后收口；把用户状态转成证据、进度、验证和回复深度。
version: 1.4.3
author: gongyu0918-debug
license: MIT
metadata:
  hermes:
    tags: [emotion-routing, coding-agent, markdown-first]
---

# Emotion Skill

Use this skill as an agent-readable playbook, not as a script-driven classifier.

The goal is to translate user-state signals into better coding-agent behavior:
show evidence sooner, keep scope tighter, recover from repeated failures, keep
progress visible during stalls, and stop expanding once the work is good.

## Core Rule

Read the user's state as a work-situation signal, then choose a behavior pattern.
Do not expose raw emotion labels to the user. Do not make a routing decision from
one keyword when the surrounding task state points elsewhere.

## When to Use

Use this skill for coding-agent work when the user's wording or task state points
to repeated failure, evidence requests, scope caution, urgent pressure, confusion,
silent progress risk, option selection, or post-success closeout.

## When Not to Use

Do not invoke it for simple one-step commands, non-coding conversation, creative
writing, or cases where no behavior change is needed. Do not run repository
scripts just to use the skill.

## Quick Workflow

1. Identify the active state pattern from the latest user turn and recent task context.
2. Load only the reference that matches the active pattern.
3. Apply the behavior rules before answering, editing, delegating, or closing out.
4. Name the evidence, scope boundary, verification step, and progress cadence when they matter.
5. If multiple patterns apply, prefer evidence and scope safety over speed.

## Routing Index

Use [references/routing-playbook.md](references/routing-playbook.md) when deciding the user's current work-state and which behavior pattern to apply.

Use [references/response-constraints.md](references/response-constraints.md) when shaping the next reply, edit boundary, progress update, or closeout.

Use [references/real-scenarios.md](references/real-scenarios.md) when validating that a change generalizes across real coding-agent failure patterns instead of fixing one example.

Use [references/subagent-forward-tests.md](references/subagent-forward-tests.md) when validating actual agent behavior with fresh subagents, especially soft constraints versus hard guardrails.

Use [references/model-prompts.md](references/model-prompts.md) when a host or agent framework needs compact prompt snippets.

Use [references/integration-openclaw-hermes.md](references/integration-openclaw-hermes.md) only when integrating this playbook into an OpenClaw/Hermes host.

Use [references/examples.md](references/examples.md) for quick before/after behavior examples.

Use [references/emotion-value-model.md](references/emotion-value-model.md) for the rationale behind this skill's behavior changes.

## Default Behavior Map

| State pattern | Prefer | Avoid |
|---|---|---|
| Repeated failure or user says it is still broken | repair first, smallest failing path, visible progress | more explanation before checking |
| Evidence request or root-cause challenge | basis first, exact command/log/file/check, then conclusion | guessing or broad claims |
| Scope protection or caution | verify boundary, state allowed files, name rollback path | adjacent refactors |
| Urgent pressure without enough evidence | shortest reliable basis, action first, tight update cadence | long preamble or background-only work |
| Confusion or path ambiguity | restate target, give one correctable default path | multiple unranked options |
| Silent delay or stuck tool/queue | status update, current blocker, next observable checkpoint | quiet background work |
| Exploratory option selection | ranked options with tradeoffs, clear recommendation when useful | forced single path without comparison |
| Post-success closeout | summarize change, run regression/smoke, stop expansion | new features or cleanup |

## Common Pitfalls

- Treat scope and evidence rules as soft constraints that shape work, not as a
  reason to refuse a justified helper file after evidence is shown.
- Do not say a file, log, or test proves something unless it was actually
  inspected.
- When the user asks for status or timing, give the next observable checkpoint or
  time bound instead of a vague progress note.
- Keep exploratory comparisons ranked; do not turn brainstorming into an
  irreversible edit path.

## Reply Contract

When this skill is active, the next visible reply should include the useful subset of:

- what state pattern is driving the behavior
- what evidence or verification point comes first
- what files, scope, or boundaries are protected
- what will be checked before declaring success
- when the user will next see progress on long-running work

Keep the language natural. Do not say the user is "frustrated" unless they used that wording or asked for classification.

## Scripts Boundary

The skill behavior lives in Markdown. Scripts in the GitHub repository are maintainer
validation tools only. Do not require a ClawHub user or an agent to execute Python
before applying this skill.

Run repository scripts only for release checks, regression comparison, or local
maintenance of this skill package.

## Published Bundle

ClawHub publish now ships the Markdown-first skill bundle:

- `SKILL.md`
- `LICENSE`
- `agents/openai.yaml`
- `references/routing-playbook.md`
- `references/response-constraints.md`
- `references/real-scenarios.md`
- `references/subagent-forward-tests.md`
- `references/model-prompts.md`
- `references/integration-openclaw-hermes.md`
- `references/examples.md`
- `references/emotion-value-model.md`

The GitHub repository keeps dev-only scripts, historical runtime experiments, audits,
and calibration files outside the installed skill bundle.

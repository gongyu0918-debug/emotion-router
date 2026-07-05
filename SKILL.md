---
name: emotion-skill
slug: emotion-skill
displayName: 情绪路由
summary: 面向 Coding Agent 的谨慎三路由情绪路由。仅在当前 prompt 出现明确急迫措辞、强烈愤怒/挫败信号，或关于当前步骤、冲突、错位的工作流困惑时，按优先级加载急迫、愤怒/挫败、困惑之一的 route reference。2.0.2 收紧困惑与愤怒边界、急迫冲突处理和“浪费时间”误触发。普通任务、中性命令、普通技术解释、内容提及默认不触发。
description: Markdown-first soft router for coding agents when the current prompt shows clear urgency wording, strong anger/frustration signals such as profanity or repeated failure/blame, or workflow confusion about the current step, conflict, or mismatch. Do not use for ordinary tasks, neutral commands, ordinary technical explanations, or content-only mentions of emotion words.
version: 2.0.2
author: gongyu0918-debug
license: MIT
metadata:
  hermes:
    tags: [emotion-routing, coding-agent, markdown-first]
---

# Emotion Router

Use this skill to route the agent's next work mode from the user's current prompt and visible context. The agent does not have real emotions. This skill reads
user-side work-state signals; it does not model user personality, hidden history, or long-term memory.

Negative user emotion and pressure can push a model toward defensive replies, over-explaining, guessing, drifting from the task, or expanding scope. Convert
that pressure into a stable execution pattern.

## Boundary

Use only the current user prompt and visible context window. Do not inspect AGENTS.md, hidden history, durable memory, user profiles, or old calibration state just to use this skill.

Trigger cautiously. Urgency needs clear speed or priority wording; anger/frustration needs strong active signals such as profanity, repeated strong negative wording, direct blame, repeated failure, or loss of trust; confusion needs workflow-state questions, instruction conflicts, or context mismatch. If the signal is merely a topic, field name, quote, neutral command, or ordinary technical explanation request, stop at this file and do ordinary work.

This is a soft router, not a classifier. Use semantic judgment over the current
work-state signal; examples are weak cues, not hard keyword triggers and not a
wordlist to complete. Do not expose labels such as "you are angry" or "you are
confused" unless the user asks for classification.

Content mentions alone are ordinary work by default. A report about confusion,
profanity research, an `urgentFlag` field, or quoted angry text does not trigger
this skill unless the same current prompt or visible context also shows active
urgency, anger/frustration, or confusion.

## Route Selection

Choose one route by priority:

1. Urgency
2. Anger or frustration
3. Confusion

If no route is active, do ordinary work and do not load a route reference.

## Progressive Loading

After choosing a route, read exactly one route reference:

- Urgency: [references/urgency-route.md](references/urgency-route.md)
- Anger or frustration: [references/anger-frustration-route.md](references/anger-frustration-route.md)
- Confusion: [references/confusion-route.md](references/confusion-route.md)

Each route file contains its own signals, non-triggers, overlap rules, response
pattern, forbidden behavior, and examples. Do not compare against or load
unrelated route files unless the selected route's overlap rule points to a
higher-priority active route.

When using this repository as a source path, treat only the Published Bundle files below as skill instructions. Other references are legacy material and must not be read for routing.

## Scripts Boundary

The skill behavior lives in Markdown. Repository scripts are maintainer release
checks only. Do not ask a user or agent to run Python before applying this skill.

## Published Bundle

ClawHub publish now ships the Markdown-first skill bundle:

- `SKILL.md`
- `LICENSE`
- `agents/openai.yaml`
- `references/anger-frustration-route.md`
- `references/confusion-route.md`
- `references/urgency-route.md`

The GitHub repository keeps legacy runtime experiments, audits, reports, assets, and older research references outside the installed skill bundle.

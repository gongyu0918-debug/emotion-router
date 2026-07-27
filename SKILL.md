---
name: emotion-skill
slug: emotion-skill
displayName: 情绪路由
summary: 面向 Coding Agent 的 Markdown-first 三路由软路由。仅当当前 prompt 或可见上下文中出现明确急迫、针对当前工作的强烈愤怒或挫败，或对正在进行的工作流感到困惑时使用；普通任务、中性命令、技术解释以及仅作为内容提及或引用的情绪词不触发。
description: 面向 Coding Agent 的 Markdown-first 软路由。当前 prompt 或可见上下文明确表现出急迫、针对当前工作的强烈愤怒或挫败，或对正在进行的工作流感到困惑时使用。普通任务、中性命令、技术解释以及仅作为内容提及或引用的情绪词不触发。
version: "2.0.6"
license: MIT
metadata:
  version: "2.0.6"
  author: gongyu0918-debug
  hermes:
    tags: [emotion-routing, coding-agent, markdown-first]
---

# Emotion Router

Route only the user's current work-state signal. Do not infer personality, inspect
hidden history or memory, or describe the user with an emotion label.

## Gate

Trigger cautiously from the current prompt and visible context:

- urgency: explicit speed, deadline, blocking, or priority pressure;
- anger/frustration: strong active hostility, blame, repeated failure, loss of
  trust, or a permission challenge;
- confusion: uncertainty about the active step, blocker, instruction conflict,
  or workflow mismatch.

Use semantic judgment; examples are cues, not a keyword or profanity list.

A topic, quote, field name, neutral command, or ordinary technical explanation is
ordinary work. Do not route it.

## Select One Route

Use this priority:

1. Urgency
2. Anger or frustration
3. Confusion

Exception: a permission challenge, unauthorized change, or demand to stop the
current action selects anger/frustration even when urgency is present.

Read exactly one reference:

- [Urgency](references/urgency-route.md)
- [Anger or frustration](references/anger-frustration-route.md)
- [Confusion](references/confusion-route.md)

If no route is active, continue ordinary work without loading a reference.

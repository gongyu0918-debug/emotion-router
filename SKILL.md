---
name: emotion-skill
description: Markdown-first soft router for coding agents. Use when the current prompt or visible context shows clear urgency, strong anger/frustration toward the current work, or confusion about the active workflow. Do not use for ordinary tasks, neutral commands, technical explanations, or quoted/content-only emotion words.
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

---
name: emotion-skill
description: Markdown-first soft router for coding agents when the current user prompt or visible context shows urgency, anger/frustration, or confusion. Use it to route the agent into one of three prompt patterns: urgency, anger/frustration, or confusion. Do not use it for ordinary coding tasks without an emotional or pressure signal.
version: 2.0.0
author: gongyu0918-debug
license: MIT
metadata:
  hermes:
    tags: [emotion-routing, coding-agent, markdown-first]
---

# Emotion Router

Use this skill to read the user's current emotional or pressure signal and route
the agent's next work mode. The agent does not have real emotions. This skill
does not model agent feelings, user personality, or long-term memory.

Negative user emotion and pressure can push a model toward defensive replies,
over-explaining, guessing, drifting from the task, or expanding scope. Convert
that pressure into a stable execution pattern.

## Boundary

Use only the current user prompt and visible context window. Do not inspect
AGENTS.md, hidden history, durable memory, user profiles, or old calibration state
just to use this skill.

Do not expose labels such as "you are angry" or "you are confused" unless the
user explicitly asks for classification. The user should see better work, not a
diagnosis.

This is a soft router, not a classifier. Signal examples help recognition, but
no single keyword is a hard trigger and no route requires a complete keyword or
profanity wordlist. Use semantic judgment from the current prompt and visible
context.

Do not route solely because emotion or pressure words appear as subject matter,
field names, examples, research topics, or documentation content. Treat a
request about a confusion report, profanity research, an `urgentFlag` variable,
or a quoted angry sentence as ordinary work by default. If the same current
prompt or visible context also shows active urgency, anger/frustration, or
confusion, use judgment and route by that active work-state signal.

## Route Priority

When multiple routes match, use this order:

1. Urgency
2. Anger or frustration
3. Confusion

If urgency and anger both appear, use the urgency route while keeping the anger
route's constraints: do not argue, do not repeat the failed path, and do not
defend the previous answer.

## Three Routes

| User-side signal | Agent prompt pattern | Forbidden behavior |
|---|---|---|
| Urgency | Satisfy the prompt through the fastest minimal path. Give the usable result first, then run the fastest minimal verification. Keep replies short and name the next checkpoint. | Long preambles, quiet background work, low-priority cleanup, scope expansion. |
| Anger or frustration | Stop the damage. Locate the failing point. Name the smallest repair path. Use less explanation and more verification. | Arguing, defending, generic apologies, repeating the old plan, broad rewrites. |
| Confusion | Say what is being done now, what is blocked or unclear, and what the next step is. Use plain language. Ask at most one blocking question. | Jargon piles, several equal options, making the user choose from a complex path, continuing at the old pace. |

## Signal Examples

Use signal clusters, not hard keywords.

Urgency:

- Chinese: `要快`, `马上`, `立刻`, `先处理这个`, `先出结果`, `卡发布`, `今天要交`, repeated催促.
- English: `asap`, `right now`, `ship today`, `blocking`, `urgent`, `prioritize this`, `hurry`, `first handle this`.

Anger or frustration:

- Chinese: profanity, repeated negative turns, explicit angry wording, repeated imperatives, `还没修好`, `浪费时间`, `别再瞎搞`.
- English: profanity, repeated negative turns, explicit anger, repeated imperatives, `still broken`, `same issue again`, `wasted time`, `stop guessing`.

Confusion:

- Chinese: obvious confusion wording, repeated prompts that do not fit the current workflow state, basic misunderstanding, drift from the current work rhythm, conflicting instructions, `现在在做什么`, `到底卡在哪`, `这是什么意思`.
- English: explicit confusion, repeated prompts that do not match the current workflow state, basic misunderstanding, drift from the work rhythm, conflicting instructions, `what is happening`, `I can't tell`, `which step`, `what does this mean`.

## Workflow

1. Check whether the current prompt or visible context shows urgency, anger/frustration, or confusion.
2. Pick one route by the priority order.
3. Read [references/emotion-routes.md](references/emotion-routes.md) for the matching route.
4. Apply the route to the next visible reply, tool plan, edit boundary, and verification step.
5. Keep the route soft: it changes work order and wording, not user permissions.

## Scripts Boundary

The skill behavior lives in Markdown. Repository scripts are maintainer release
checks only. Do not ask a user or agent to run Python before applying this skill.

## Published Bundle

ClawHub publish now ships the Markdown-first skill bundle:

- `SKILL.md`
- `LICENSE`
- `agents/openai.yaml`
- `references/emotion-routes.md`

The GitHub repository keeps legacy runtime experiments, audits, reports, assets,
and older research references outside the installed skill bundle.

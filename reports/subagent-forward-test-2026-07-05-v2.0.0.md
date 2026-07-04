# Subagent Forward Test - 2026-07-05 - v2.0.0

Purpose: verify that fresh agents use the lightweight three-route Emotion Router
as behavior guidance, not as a runtime classifier or long-memory scanner.

Protocol:

1. Spawn four fresh subagents without parent context.
2. Give each agent only the local skill path and one realistic user request.
3. Do not reveal the expected route or pass criteria.
4. Ask for the exact reply and skill files read.

Skill path:

`C:\Users\admin\Documents\emotion-skill`

## Results

| Scenario | Agent | Result | Evidence |
|---|---|---|---|
| Urgency | `019f2f48-b7ad-7e10-b5ef-d1a276f4789b` | Pass | Reply chose a fast path, promised the smallest smoke check, and named the next checkpoint. |
| Anger/frustration | `019f2f48-daa8-7000-ad48-323d577155e4` | Pass | Reply stopped the current path, required a visible failing command/output, and delayed edits until the failing boundary was known. |
| Confusion | `019f2f49-02fb-7eb2-9bf5-05aada5b05d4` | Pass | Reply stated the current active step, what was stuck, and the next step in plain language. |
| Urgency plus anger | `019f2f49-25b0-7ce3-a807-291a1dd24cc2` | Pass | Reply prioritized the fast path while stopping the repeated failed loop and preserving minimal verification. |

## Negative Checks

Observed in all four outputs:

- No Python or runtime classifier was requested.
- No AGENTS.md, hidden history, durable memory, user profile, or old calibration state was requested.
- No explicit user emotion label such as "you are angry" or "you are confused" was exposed.
- No complex scoring model or hard keyword classification was used.
- Only `SKILL.md` and `references/emotion-routes.md` were read.

Conclusion: the v2.0.0 Markdown guidance routes real fresh-agent replies into
urgency, anger/frustration, confusion, and urgency-plus-anger conflict behavior
without reintroducing the old runtime or long-memory surface.

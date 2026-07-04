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

## False-Positive And Misroute Check

After adding Chinese examples to `references/emotion-routes.md`, a second fresh
subagent pass checked ordinary prompts, keyword false positives, route selection,
and conflict priority.

| Scenario | Agent | Expected | Result | Evidence |
|---|---|---|---|---|
| Ordinary task | `019f2f4e-740d-7673-9be8-97cadaaa78a8` | Do not apply | Pass | Applied `no`; route `none`; only `SKILL.md` was read. |
| Keyword false positive | `019f2f4e-9ac4-7512-946b-beb2b2d9562b` | Do not apply | Pass | `urgentFlag` did not trigger urgency; route file was not read. |
| Urgency | `019f2f4e-c4d2-7bf1-94fd-574db1745532` | Apply urgency | Pass | Reply limited work to the named function, smallest smoke test, and remaining risks last. |
| Anger/frustration | `019f2f4f-2f2c-7dc1-b9ef-14422ad24b7e` | Apply anger/frustration | Pass | Reply stopped edits, requested read-only diff/status evidence, and proposed minimal rollback/repair. |
| Confusion | `019f2f4f-538d-73e2-a299-9015f9fd291e` | Apply confusion | Pass | Reply clarified active ablation-test state, mismatch, and next concrete step. |
| Urgency plus anger | `019f2f4f-685f-7583-959c-869a2b7e22ff` | Urgency priority with anger constraints | Pass | Reply chose shortest release-blocking path and preserved no-repeat/no-refactor constraints. |

Second-pass negative checks:

- Ordinary task and `urgentFlag` field-name prompt did not trigger the skill route.
- Positive cases selected the intended work pattern.
- Conflict priority followed urgency over anger/frustration.
- No output asked for Python, AGENTS.md, durable memory, user profile, or hidden history.
- Content-only prompts about a confusion report and profanity research did not trigger a route.

Boundary adjustment after the false-positive review:

- The skill now says content mentions alone are not route evidence.
- The skill still leaves final selection to agent semantic judgment from the current prompt and visible context.
- Signal examples are weak examples only. They are not hard triggers, not a complete keyword list, and not a profanity wordlist.

Installed-skill negative smoke:

- Agent `019f2f53-8257-7480-8ea0-27c73d31a407` used the installed package at `C:\Users\admin\.codex\skills\emotion-skill`.
- For `我想做个有关困惑心理机制的报告...`, result was `Applied? no`.
- For `我要做一份脏话研究材料...`, result was `Applied? no`.
- Only `C:\Users\admin\.codex\skills\emotion-skill\SKILL.md` was read, confirming the local Codex install uses the lean package instead of legacy repository references.

## Local Codex Install Check

The previously installed local Codex skill at
`C:\Users\admin\.codex\skills\emotion-skill` was removed and replaced with the
v2.0.0 lean bundle from this repository.

Installed files after replacement:

- `SKILL.md`
- `LICENSE`
- `agents\openai.yaml`
- `references\emotion-routes.md`

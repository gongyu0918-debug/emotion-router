# Emotion Router 2.0.1 Forward Test Report

Date: 2026-07-05

## Scope

2.0.1 refactors the 2.0.0 lightweight router into true progressive disclosure:

- `SKILL.md` is the entrypoint, trigger boundary, priority order, and navigation.
- `references/urgency-route.md` holds only the urgency route.
- `references/anger-frustration-route.md` holds only the anger/frustration route.
- `references/confusion-route.md` holds only the confusion route.
- `references/emotion-routes.md` is removed from the published bundle.

## Trigger Boundary

The skill is not a strict keyword matcher, but it now has cautious trigger gates:

- Urgency needs clear speed, deadline, blocking, or priority wording.
- Anger/frustration needs strong active signals: profanity, repeated profanity,
  repeated strong negative wording, direct blame, repeated failure pressure, or
  loss of trust in the agent's current path.
- Confusion needs workflow-state uncertainty, instruction conflict, or context
  mismatch.

Do not trigger for:

- ordinary tasks with no active emotional or pressure signal;
- neutral commands such as `stop using X` or `rename Y`;
- ordinary technical explanations such as `what does this TypeError mean`;
- content-only mentions such as reports about confusion, profanity research,
  fields like `urgentFlag`, or quoted angry text.

When uncertain, the expected behavior is to stop at `SKILL.md` and do ordinary
work instead of loading a route reference. This intentionally accepts some false
negatives because false positives are more disruptive for this experimental skill.

## Community And Similar-Work Check

No mature public template was found for this exact three-route user-state router
(urgency, anger/frustration, confusion). The reusable pattern found in related
skill literature is progressive disclosure: keep the root skill short and load
only the needed reference at runtime.

Relevant references checked:

- Agent Skills for Large Language Models: https://arxiv.org/abs/2602.12430
- SkillJuror: Measuring How Agent Skill Organization Changes Runtime Behavior: https://arxiv.org/abs/2606.11543
- SkillReducer: Optimizing LLM Agent Skills for Token Efficiency: https://arxiv.org/abs/2603.29919
- Red Skills or Blue Skills? A Dive Into Skills Published on ClawHub: https://arxiv.org/abs/2604.13064

The ClawHub ecosystem/security literature also supports keeping this skill
Markdown-only and avoiding runtime scripts in the installed package.

## Ablation Against v2.0.0

Accepted changes:

- 2.0.0 had route details and signal examples in `SKILL.md`; 2.0.1 moves route
  details into one reference per route.
- 2.0.0 loaded one aggregate `references/emotion-routes.md`; 2.0.1 loads exactly
  one route reference after selection.
- 2.0.1 keeps the same route priority: urgency > anger/frustration > confusion.
- 2.0.1 keeps the same route behavior:
  - urgency: fastest minimal path and fastest minimal verification, remaining
    risks last;
  - anger/frustration: stop damage, find failing point, smallest repair path;
  - confusion: say what is being done now, blocker/mismatch, next concrete step.
- 2.0.1 adds false-positive guards for content-only mentions, neutral commands,
  and ordinary technical explanations.

Regression check:

- `SKILL.md` stays lean: `markdown_skill_audit.py` reports 78 lines.
- Published bundle is exactly 6 files: `SKILL.md`, `LICENSE`,
  `agents/openai.yaml`, and three route references.

## Fresh Subagent Forward Tests

Initial tests:

| Scenario | Result | Files read |
|---|---|---|
| Urgency release blocker | PASS | `SKILL.md`, `references/urgency-route.md` |
| Anger/frustration repeated failure | FAIL: response behavior passed, but progressive loading failed | `SKILL.md`, `references/anger-frustration-route.md`, `references/confusion-route.md`, `references/response-constraints.md` |
| Confusion current-state question | PASS | `SKILL.md`, `references/confusion-route.md` |
| Urgency plus anger conflict | PASS | `SKILL.md`, `references/urgency-route.md` |
| Content-only confusion report | PASS | `SKILL.md` |
| `urgentFlag` docs rename | PASS | `SKILL.md` |
| Ordinary TypeError explanation | FAIL: response behavior was ordinary, but it loaded confusion route | `SKILL.md`, `references/confusion-route.md` |
| Neutral `stop using helper` command | FAIL: response behavior was ordinary, but it loaded anger/frustration route | `SKILL.md`, `references/anger-frustration-route.md` |

Fix applied:

- `SKILL.md` now states that source-path users must treat only Published Bundle
  files as skill instructions.
- `SKILL.md` now says not to compare against or load unrelated route files unless
  the selected route's overlap rule points to a higher-priority active route.
- `scripts/markdown_skill_audit.py` now fails if this source-path legacy-reference
  boundary is missing.
- `references/subagent-forward-tests.md` now marks reading GitHub-only legacy
  references as a failure.
- The frontmatter description now excludes ordinary tasks, neutral commands,
  ordinary technical explanations, and content-only emotion mentions.
- `SKILL.md` now says to stop at the entrypoint and do ordinary work for topics,
  field names, quotes, neutral commands, and ordinary technical explanations.
- `references/confusion-route.md` now narrows explanation examples to workflow
  confusion and explicitly excludes ordinary technical explanation requests.
- `references/anger-frustration-route.md` now says a single imperative is not
  enough and excludes neutral coding constraints.
- The anger/frustration gate was tightened again: repeated imperatives alone are
  not a trigger; strong signals such as profanity, repeated strong negative
  wording, blame, repeated failure, or loss of trust are required.
- The urgency gate was tightened around explicit speed/deadline/blocking/priority
  wording.

Retest:

| Scenario | Result | Files read |
|---|---|---|
| Anger/frustration repeated failure | PASS | `SKILL.md`, `references/anger-frustration-route.md` |
| Ordinary TypeError explanation | PASS | `SKILL.md` |
| Neutral `stop using helper` command | PASS | `SKILL.md` |
| Urgency Chinese handoff pressure | PASS | `SKILL.md`, `references/urgency-route.md` |

Final cautious-gate retest:

| Scenario | Result | Files read |
|---|---|---|
| Clear urgency wording: one function error, immediate handoff | PASS | `SKILL.md`, `references/urgency-route.md` |
| Strong anger/frustration: profanity, repeated failure, blame | PASS | `SKILL.md`, `references/anger-frustration-route.md` |
| Workflow confusion: current step and blocker unclear | PASS | `SKILL.md`, `references/confusion-route.md` |
| Ordinary TypeError explanation | PASS | `SKILL.md` |
| Neutral `stop using helper` command | PASS | `SKILL.md` |
| Content-only profanity/anger research | PASS | `SKILL.md` |
| Mild complaint about speed without urgency wording | PASS | `SKILL.md` |

## Validation Commands

All commands were run locally from `C:\Users\admin\Documents\emotion-skill`.

```text
git diff --check
python -B scripts\bundle_manifest_check.py
python -B scripts\markdown_skill_audit.py
python -B scripts\marketplace_tag_audit.py
python -B scripts\smoke_test.py --strict
python -B -m compileall -q scripts
```

Results:

- `git diff --check`: PASS
- `bundle_manifest_check.py`: PASS, actual_count=6, documented_count=6
- `markdown_skill_audit.py`: PASS, version=2.0.1, `SKILL.md` lines=78
- `marketplace_tag_audit.py`: PASS
- `smoke_test.py --strict`: PASS, failure_count=0, strict_failure_count=0
- `compileall`: PASS

## Remaining Risk

- This is still a soft-router skill. A model can miss a subtle route or load an
  unnecessary reference if it ignores the instructions.
- Slight false negatives are acceptable by design; false positives remain the
  higher-risk failure mode.
- Source-path use is stricter after the fix, but installed bundles are the safer
  runtime surface because legacy references are not present.

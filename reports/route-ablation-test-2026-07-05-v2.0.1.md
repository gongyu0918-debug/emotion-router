# Emotion Router 2.0.1 Route Ablation Test

Date: 2026-07-05

## Goal

Strengthen the release check for whether Emotion Router 2.0.1 can trigger the
intended boundaries and whether a recorded skill-applied response fixture is
better than a no-skill baseline. This test focuses on the current Markdown skill
contract, not the legacy runtime classifier.

## Method

Three checks were added:

1. Markdown contract checks for `SKILL.md` and the three route references.
2. Deterministic route-gate matrix in `scripts/route_ablation_test.py`.
3. Recorded fresh subagent A/B response fixture:
   - Baseline agent: did not read skill files.
   - Skill agent: read `SKILL.md` and the active route references.
   - Both answered the same eight prompts.

The A/B score checks whether the recorded first response better follows the
intended execution strategy. It does not reward exposing emotion labels. This is
a reproducible fixture replay of fresh subagent outputs, not an automated live
LLM benchmark.

## Route-Gate Coverage

The matrix covers:

- Urgency: clear speed, delivery, blocking, or priority cues.
- Anger/frustration: profanity, blame, repeated failure, stop-guessing pressure.
- Confusion: current step, blocker, next step, and instruction conflict.
- Overlaps: urgency > anger/frustration > confusion.
- Mixed cases: `urgentFlag` or `stop using helper` plus active urgency should
  still trigger urgency.
- Non-triggers: content-only emotion topics, profanity research, field names by
  themselves, ordinary TypeError explanations, neutral `stop using helper`
  commands, mild feedback, importance without speed pressure, repeated
  imperatives alone, negated urgency, and negated blocking release.

## Fresh Subagent A/B Summary

The skill condition improved the highest-risk cases:

- Urgency prompts gained explicit fast-path language, narrow scope, and minimal
  verification.
- Anger/frustration prompts gained stop-current-work, changed-file accounting,
  and confirm-before-more-writes behavior.
- Ordinary prompts stayed ordinary in the recorded fixture: no route label
  leakage and no urgency/anger/confusion response shape for content-only or
  neutral technical requests.

The no-skill baseline was not bad, but it was less consistent on route-specific
execution patterns. The confusion case was roughly equal because a normal coding
agent can often explain current state without the skill.

## Validation Command

```text
python -B scripts\route_ablation_test.py
```

Expected result:

- Route gate: all cases pass.
- A/B fixture replay: skill score higher than baseline, with no per-case
  regression.

Observed result:

- Markdown contract: all checks passed.
- Route gate: 22/22 passed.
- No-skill baseline fixture: 34/38 checks passed, rate 0.8947.
- Skill condition fixture: 38/38 checks passed, rate 1.0000.
- Recorded fixture improvement: +0.1053.
- Skill-better cases: urgency delivery, anger/permission challenge, and
  urgency plus repeated-failure overlap.
- Skill regressions: none.

## Remaining Risk

This is still a soft prompt-reference skill. The script checks the Markdown
contract, a deterministic evaluator for the documented boundary, and recorded
fresh-agent A/B outputs. It does not itself call a live model. A future model can
still miss a subtle trigger or ignore the progressive-loading instruction. The
intended tradeoff remains: avoid false positives even if mild false negatives
occur.

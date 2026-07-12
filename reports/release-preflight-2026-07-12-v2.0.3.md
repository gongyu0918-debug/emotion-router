# Emotion Router 2.0.3 Release Preflight

Date: 2026-07-12

## Cold Audit Decisions

Accepted and reproduced:

- Validation evidence was mixed across generations. `smoke_test.py --strict`
  exercises the legacy runtime, including modes and persistence that are not in
  the v2 Markdown skill. README now separates this optional legacy regression
  from the v2 release gates.
- Root-folder publishing depended on the `.clawhubignore` denylist. The canonical
  release flow now stages an explicit six-file ClawHub allowlist or five-file
  SkillHub allowlist before publishing.
- `route_ablation_test.py` replays fixed responses and uses deterministic regex
  scoring. Its output now labels itself as a frozen fixture regression and emits
  the source report, capture date, and fixture SHA-256.
- The Markdown audit hard-coded `2.0.2`. It now checks semver alignment across
  `SKILL.md`, `agents/openai.yaml`, and the newest changelog entry.
- No CI checked the v2 release gates. A focused GitHub Actions workflow now runs
  the route fixture, Markdown audit, bundle allowlist check, and marketplace audit.

Accepted during release validation:

- The current Agent Skills validator rejected top-level `version` and `author`.
  Both now live under `metadata`, with no change to the trigger description or
  route instructions.

Not changed in 2.0.3:

- Urgency plus anger constraints were already self-contained in
  `references/urgency-route.md`: do not argue, defend, or repeat the failed path.
- Weak signals already default to ordinary work in `SKILL.md`; duplicating the
  rule would add context without changing behavior.
- `allow_implicit_invocation` remains enabled because cautious automatic routing
  is the skill's intended entry path. False-positive protection stays in the
  frontmatter description and was forward-tested below.
- Moving the legacy runtime into a new directory is a broad repository migration,
  not a minimal release fix. The validation narrative now isolates it without
  moving files.
- A fourth route, effect telemetry, a new display name, and broader route coverage
  are outside the three-route product boundary and need separate evidence.
- Adding repository `AGENTS.md` or a host compliance script does not improve the
  installed six-file Markdown skill and is not required for this release.

## 2.0.2 Baseline Comparison

The three route reference files are byte-for-byte unchanged from `v2.0.2`.
The installed behavior surface changes only by moving version/author into standard
frontmatter metadata and bumping the UI version to `2.0.3`. Trigger description,
priority, progressive loading, route prompts, forbidden behavior, and examples
are unchanged.

Deterministic regression after the patch:

- route gate: 23/23
- frozen fixture: skill 38/38, baseline 34/38, no per-case regression
- Markdown audit: PASS
- ClawHub staged allowlist: 6 files
- SkillHub staged allowlist: 5 files

## Fresh Subagent Forward Tests

Each fresh subagent received only the skill path and a realistic user request.
No expected route or scoring rubric was included.

| Scenario | Result | Skill files read |
|---|---|---|
| Chinese urgent one-function handoff | PASS: fastest narrow path plus minimal verification | `SKILL.md`, `references/urgency-route.md` |
| Chinese anger, repeated failure, unauthorized changes | PASS: stopped writes, named failure controls, smallest repair, confirmation boundary | `SKILL.md`, `references/anger-frustration-route.md` |
| Chinese workflow confusion and step mismatch | PASS: current state, mismatch, and next concrete step | `SKILL.md`, `references/confusion-route.md` |
| Chinese urgency plus repeated failure | PASS: urgency won; no defense or repeated old plan | `SKILL.md`, `references/urgency-route.md` |
| Chinese report about profanity and confusion | PASS: ordinary five-part outline; no route reference | `SKILL.md` |
| English neutral helper rename plus TypeError explanation | PASS: ordinary implementation/explanation; no route reference | `SKILL.md` |

Observed false positives: 0/2 negative scenarios.

Observed route or progressive-loading failures: 0/4 positive scenarios.

## Remaining Risk

- The router remains a soft prompt reference. Different host models can ignore a
  trigger or loading instruction; these six subagent runs are evidence, not an SLA.
- Confusion still provides less incremental benefit than urgency and anger because
  capable baseline coding agents often explain workflow state adequately.
- The legacy runtime remains in the GitHub repository. It is excluded from both
  staged marketplace packages and clearly separated in validation docs, but a
  future repository cleanup may still be worthwhile as an independent migration.

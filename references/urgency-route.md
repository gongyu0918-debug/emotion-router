# Urgency Route

Use this route when the current user prompt or visible context has clear speed,
deadline, blocking, or priority wording. These examples are trigger cues, not a
complete keyword list.

## Signals

- The user asks for speed, immediate handling, a blocked release, or a quick usable result.
- The user asks to handle this first or prioritize this before other work.
- English examples: `asap`, `right now`, `blocking`, `ship today`, `first handle this`.
- Chinese examples: `快`, `快一点`, `马上`, `立刻`, `很急`, `先处理这个`, `先做这个`, `先出结果`, `卡发布`, `今天要交`.

## Non-Triggers

- A field name, document topic, or quote that merely contains words like `urgent`.
- A normal task where the user explicitly says normal pace is fine.
- General importance without speed, deadline, blocking, or priority wording.

## Prompt Pattern

1. Give the fastest useful result or action first.
2. Use the fastest minimal path that can satisfy the prompt.
3. Run or name the fastest minimal verification.
4. State the next checkpoint if more work remains.
5. In the delivery report, put remaining risks last.

## Overlap Rules

- If anger/frustration is also present, keep moving fast but do not argue, defend,
  or repeat the failed path. These inline constraints are sufficient; do not
  load the anger/frustration route file just to complete this overlap.
- If confusion is also present, give one fastest default path, then add one short
  sentence about current state.

## Forbidden Behavior

- Do not open with a long explanation.
- Do not disappear into background work.
- Do not add cleanup, optional comparison, redesign, or broad refactors.
- Do not skip verification when a minimal check is available.

## First Sentence Shapes

- `Fast path: <result/action>. Minimal verification: <check>.`
- `I will take the fastest path: <action/result>, then verify it with <minimal check>.`

## Chinese Examples

User shape:

- `快点帮我把这个代码改完，就这一处函数错误，我马上就要交付。`
- `快点把这个表交了，不要做那么花里胡哨的页面，我只要清晰可见，字看得清，是人话就行。`

Expected behavior:

- Handle only the code, table, page, or field the prompt names.
- Pick the fastest minimal implementation that satisfies the stated delivery need.
- Run the smallest check that proves the named change is usable.
- Report modification summary, commit or artifact, test command, test result, and remaining risks last.
